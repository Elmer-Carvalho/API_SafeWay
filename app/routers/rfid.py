from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import RFIDCredential, User, AccessLog, EventType
from app.schemas import RFIDCredentialCreate, RFIDCredentialUpdate, RFIDCredential as RFIDCredentialSchema, RFIDAccessRequest, AccessLog as AccessLogSchema
import uuid
from datetime import datetime
import pytz

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
            "user_name": None,
            "user_id": None,
            "user_email": None,
            "message": "Credencial não encontrada",
            "has_time_restriction": False,
            "time_window_start": None,
            "time_window_end": None
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
            "user_name": credential.user.full_name,
            "user_id": str(credential.user_id),
            "user_email": credential.user.email,
            "message": "Usuário inativo",
            "has_time_restriction": credential.has_time_restriction,
            "time_window_start": credential.time_window_start,
            "time_window_end": credential.time_window_end
        }
    
    # Verificar restrição de horário
    if credential.has_time_restriction:
        # Obter horário atual em UTC-3 (Brasil)
        tz_brazil = pytz.timezone('America/Sao_Paulo')
        current_time = datetime.now(tz_brazil)
        current_hour_minute = current_time.strftime("%H:%M")
        
        # Converter strings de horário para minutos desde meia-noite para comparação
        def time_to_minutes(time_str):
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes
        
        current_minutes = time_to_minutes(current_hour_minute)
        start_minutes = time_to_minutes(credential.time_window_start)
        end_minutes = time_to_minutes(credential.time_window_end)
        
        # Verificar se a janela cruza meia-noite (ex: 22:00-06:00)
        if start_minutes > end_minutes:
            # Janela cruza meia-noite
            access_allowed = current_minutes >= start_minutes or current_minutes <= end_minutes
        else:
            # Janela normal
            access_allowed = start_minutes <= current_minutes <= end_minutes
        
        if not access_allowed:
            # Log de acesso negado - fora do horário
            access_log = AccessLog(
                user_id=credential.user_id,
                rfid_credential_id=credential.id,
                event_type=EventType.ACCESS_DENIED,
                location=access_request.location,
                description=f"Fora do horário permitido ({credential.time_window_start}-{credential.time_window_end})"
            )
            db.add(access_log)
            db.commit()
            
            return {
                "access_granted": False,
                "user_name": credential.user.full_name,
                "user_id": str(credential.user_id),
                "user_email": credential.user.email,
                "message": "Fora do horário permitido",
                "has_time_restriction": True,
                "time_window_start": credential.time_window_start,
                "time_window_end": credential.time_window_end
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
        "user_name": credential.user.full_name,
        "user_id": str(credential.user_id),
        "user_email": credential.user.email,
        "message": "Acesso liberado",
        "has_time_restriction": credential.has_time_restriction,
        "time_window_start": credential.time_window_start if credential.has_time_restriction else "00:00",
        "time_window_end": credential.time_window_end if credential.has_time_restriction else "23:59"
    }