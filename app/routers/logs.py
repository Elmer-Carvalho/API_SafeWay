from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models import AccessLog, ErrorLog
from app.schemas import AccessLog as AccessLogSchema, ErrorLogCreate, ErrorLog as ErrorLogSchema

router = APIRouter()

@router.get("/access", response_model=List[AccessLogSchema])
def list_access_logs(
    skip: int = 0, 
    limit: int = 100, 
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Listar logs de acesso"""
    query = db.query(AccessLog)
    
    if start_date:
        query = query.filter(AccessLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AccessLog.timestamp <= end_date)
    
    logs = query.order_by(AccessLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/access/all", response_model=List[AccessLogSchema])
def list_all_access_logs(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Listar todos os logs de acesso (sem paginação)"""
    query = db.query(AccessLog)
    
    if start_date:
        query = query.filter(AccessLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AccessLog.timestamp <= end_date)
    
    logs = query.order_by(AccessLog.timestamp.desc()).all()
    return logs

@router.get("/access/{log_id}", response_model=AccessLogSchema)
def get_access_log(log_id: str, db: Session = Depends(get_db)):
    """Obter log de acesso por ID"""
    log = db.query(AccessLog).filter(AccessLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log não encontrado")
    return log

@router.post("/errors", response_model=ErrorLogSchema)
def create_error_log(error_log: ErrorLogCreate, db: Session = Depends(get_db)):
    """Criar log de erro - endpoint para o sistema local"""
    db_error_log = ErrorLog(**error_log.dict())
    db.add(db_error_log)
    db.commit()
    db.refresh(db_error_log)
    return db_error_log

@router.get("/errors", response_model=List[ErrorLogSchema])
def list_error_logs(
    skip: int = 0, 
    limit: int = 100,
    severity: Optional[str] = None,
    component: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Listar logs de erro"""
    query = db.query(ErrorLog)
    
    if severity:
        query = query.filter(ErrorLog.severity == severity)
    if component:
        query = query.filter(ErrorLog.component == component)
    if start_date:
        query = query.filter(ErrorLog.timestamp >= start_date)
    if end_date:
        query = query.filter(ErrorLog.timestamp <= end_date)
    
    logs = query.order_by(ErrorLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/errors/all", response_model=List[ErrorLogSchema])
def list_all_error_logs(
    severity: Optional[str] = None,
    component: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Listar todos os logs de erro (sem paginação)"""
    query = db.query(ErrorLog)
    
    if severity:
        query = query.filter(ErrorLog.severity == severity)
    if component:
        query = query.filter(ErrorLog.component == component)
    if start_date:
        query = query.filter(ErrorLog.timestamp >= start_date)
    if end_date:
        query = query.filter(ErrorLog.timestamp <= end_date)
    
    logs = query.order_by(ErrorLog.timestamp.desc()).all()
    return logs

@router.get("/errors/{log_id}", response_model=ErrorLogSchema)
def get_error_log(log_id: str, db: Session = Depends(get_db)):
    """Obter log de erro por ID"""
    log = db.query(ErrorLog).filter(ErrorLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log não encontrado")
    return log
