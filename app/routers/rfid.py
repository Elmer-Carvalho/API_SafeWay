from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import RFIDCredential, User, AccessLog, EventType
from app.schemas import RFIDCredentialCreate, RFIDCredentialUpdate, RFIDCredential as RFIDCredentialSchema, RFIDAccessRequest, AccessLog as AccessLogSchema
import uuid

router = APIRouter()

@router.post("/credentials", response_model=RFIDCredentialSchema)
def create_rfid_credential(credential: RFIDCredentialCreate, db: Session = Depends(get_db)):
    """Criar nova credencial RFID"""
    # Verificar se usuário existe
    user = db.query(User).filter(User.id == credential.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verificar se card_id já existe
    existing_credential = db.query(RFIDCredential).filter(RFIDCredential.card_id == credential.card_id).first()
    if existing_credential:
        raise HTTPException(status_code=400, detail="Card ID já cadastrado")
    
    db_credential = RFIDCredential(**credential.dict())
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)
    return db_credential

@router.get("/credentials", response_model=List[RFIDCredentialSchema])
def list_rfid_credentials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar credenciais RFID"""
    credentials = db.query(RFIDCredential).offset(skip).limit(limit).all()
    return credentials

@router.get("/credentials/all", response_model=List[RFIDCredentialSchema])
def list_all_rfid_credentials(db: Session = Depends(get_db)):
    """Listar todas as credenciais RFID (sem paginação)"""
    credentials = db.query(RFIDCredential).all()
    return credentials

@router.get("/credentials/sync")
def sync_rfid_credentials(
    page: int = 1, 
    page_size: int = 40,
    db: Session = Depends(get_db)
):
    """Sincronizar credenciais RFID para dispositivos embarcados - com paginação"""
    
    # Calcular offset
    skip = (page - 1) * page_size
    
    # Buscar apenas credenciais ativas com usuários ativos
    credentials = db.query(RFIDCredential).join(User).filter(
        RFIDCredential.is_active == True,
        User.is_active == True
    ).offset(skip).limit(page_size).all()
    
    # Contar total de registros
    total = db.query(RFIDCredential).join(User).filter(
        RFIDCredential.is_active == True,
        User.is_active == True
    ).count()
    
    # Montar response
    sync_data = []
    for credential in credentials:
        sync_data.append({
            "card_id": credential.card_id,
            "user_name": credential.user.full_name,
            "has_time_restriction": False,
            "time_window_start": "00:00",
            "time_window_end": "23:59"
        })
    
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size,
        "data": sync_data
    }

@router.get("/credentials/{credential_id}", response_model=RFIDCredentialSchema)
def get_rfid_credential(credential_id: str, db: Session = Depends(get_db)):
    """Obter credencial RFID por ID"""
    credential = db.query(RFIDCredential).filter(RFIDCredential.id == credential_id).first()
    if not credential:
        raise HTTPException(status_code=404, detail="Credencial não encontrada")
    return credential

@router.put("/credentials/{credential_id}", response_model=RFIDCredentialSchema)
def update_rfid_credential(credential_id: str, credential_update: RFIDCredentialUpdate, db: Session = Depends(get_db)):
    """Atualizar credencial RFID"""
    credential = db.query(RFIDCredential).filter(RFIDCredential.id == credential_id).first()
    if not credential:
        raise HTTPException(status_code=404, detail="Credencial não encontrada")
    
    update_data = credential_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(credential, field, value)
    
    db.commit()
    db.refresh(credential)
    return credential

@router.post("/validate-access")
def validate_rfid_access(access_request: RFIDAccessRequest, db: Session = Depends(get_db)):
    """Validar acesso RFID - endpoint para o sistema local"""
    
    try:
        # Buscar credencial RFID
        credential = db.query(RFIDCredential).filter(
            RFIDCredential.card_id == access_request.card_id,
            RFIDCredential.is_active == True
        ).first()
        
        if not credential:
            # Log de acesso negado - card não encontrado
            access_log = AccessLog(
                user_id=None,
                rfid_credential_id=None,
                event_type=EventType.CARD_NOT_FOUND,
                location=access_request.location,
                description=f"Card ID {access_request.card_id} não encontrado"
            )
            db.add(access_log)
            db.commit()
            
            return {
                "access_granted": False,
                "message": "Credencial não encontrada"
            }
        
        # Verificar se usuário está ativo
        if not credential.user.is_active:
            # Log de acesso negado - usuário inativo
            access_log = AccessLog(
                user_id=credential.user_id,
                rfid_credential_id=credential.id,
                event_type=EventType.ACCESS_DENIED,
                location=access_request.location,
                description="Usuário inativo"
            )
            db.add(access_log)
            db.commit()
            
            return {
                "access_granted": False,
                "message": "Usuário inativo"
            }
        
        # Acesso concedido
        access_log = AccessLog(
            user_id=credential.user_id,
            rfid_credential_id=credential.id,
            event_type=EventType.ACCESS_GRANTED,
            location=access_request.location,
            description=f"Acesso concedido para {credential.user.full_name}"
        )
        db.add(access_log)
        db.commit()
        
        return {
            "access_granted": True,
            "user": {
                "id": str(credential.user.id),
                "name": credential.user.full_name,
                "email": credential.user.email
            },
            "message": "Acesso concedido"
        }
        
    except Exception as e:
        db.rollback()
        # Log de erro para debug
        print(f"Erro ao validar acesso: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao processar validação de acesso: {str(e)}"
        )
