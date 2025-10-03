from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models import AccessLog, ErrorLog, HttpLog
from app.schemas import (
    AccessLog as AccessLogSchema,
    ErrorLog as ErrorLogSchema,
    ErrorLogCreate,
    HttpLog as HttpLogSchema
)

router = APIRouter()

# --------------------------
# Logs de Acesso
# --------------------------
@router.get("/access", response_model=List[AccessLogSchema])
def list_access_logs(
    skip: int = 0, 
    limit: int = 100, 
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(AccessLog)
    if start_date:
        query = query.filter(AccessLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AccessLog.timestamp <= end_date)
    return query.order_by(AccessLog.timestamp.desc()).offset(skip).limit(limit).all()

@router.get("/access/all", response_model=List[AccessLogSchema])
def list_all_access_logs(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(AccessLog)
    if start_date:
        query = query.filter(AccessLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AccessLog.timestamp <= end_date)
    return query.order_by(AccessLog.timestamp.desc()).all()

@router.get("/access/{log_id}", response_model=AccessLogSchema)
def get_access_log(log_id: str, db: Session = Depends(get_db)):
    log = db.query(AccessLog).filter(AccessLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log não encontrado")
    return log

# --------------------------
# Logs de Erros
# --------------------------
@router.post("/errors", response_model=ErrorLogSchema)
def create_error_log(error_log: ErrorLogCreate, db: Session = Depends(get_db)):
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
    query = db.query(ErrorLog)
    if severity:
        query = query.filter(ErrorLog.severity == severity)
    if component:
        query = query.filter(ErrorLog.component == component)
    if start_date:
        query = query.filter(ErrorLog.timestamp >= start_date)
    if end_date:
        query = query.filter(ErrorLog.timestamp <= end_date)
    return query.order_by(ErrorLog.timestamp.desc()).offset(skip).limit(limit).all()

@router.get("/errors/all", response_model=List[ErrorLogSchema])
def list_all_error_logs(
    severity: Optional[str] = None,
    component: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ErrorLog)
    if severity:
        query = query.filter(ErrorLog.severity == severity)
    if component:
        query = query.filter(ErrorLog.component == component)
    if start_date:
        query = query.filter(ErrorLog.timestamp >= start_date)
    if end_date:
        query = query.filter(ErrorLog.timestamp <= end_date)
    return query.order_by(ErrorLog.timestamp.desc()).all()

@router.get("/errors/{log_id}", response_model=ErrorLogSchema)
def get_error_log(log_id: str, db: Session = Depends(get_db)):
    log = db.query(ErrorLog).filter(ErrorLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log não encontrado")
    return log

# --------------------------
# Logs HTTP
# --------------------------
@router.get("/http", response_model=List[HttpLogSchema])
def list_http_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar logs de requisições HTTP (middleware)"""
    logs = db.query(HttpLog).order_by(HttpLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs
