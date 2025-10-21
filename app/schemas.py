from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models import EventType, ErrorSeverity
import uuid

# Schemas para User
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    is_active: bool = True

    has_time_restriction: bool = False
    time_window_start: str = "00:00"
    time_window_end: str = "23:59"

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

    has_time_restriction: Optional[bool] = None
    time_window_start: Optional[str] = None
    time_window_end: Optional[str] = None

class User(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schemas para RFID Credential
class RFIDCredentialBase(BaseModel):
    card_id: str
    is_active: bool = True

class RFIDCredentialCreate(RFIDCredentialBase):
    user_id: uuid.UUID

class RFIDCredentialUpdate(BaseModel):
    card_id: Optional[str] = None
    is_active: Optional[bool] = None

class RFIDCredential(RFIDCredentialBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schemas para Access Log
class AccessLogBase(BaseModel):
    event_type: EventType
    location: str
    description: Optional[str] = None

class AccessLogCreate(AccessLogBase):
    user_id: uuid.UUID
    rfid_credential_id: uuid.UUID

class AccessLog(AccessLogBase):
    id: uuid.UUID
    user_id: uuid.UUID
    rfid_credential_id: uuid.UUID
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Schemas para Error Log
class ErrorLogBase(BaseModel):
    error_type: str
    component: str
    description: str
    severity: ErrorSeverity

class ErrorLogCreate(ErrorLogBase):
    pass

class ErrorLog(ErrorLogBase):
    id: uuid.UUID
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Schemas para HTTP Log
class HttpLogBase(BaseModel):
    method: str
    endpoint: str
    status_code: int
    payload: Optional[str] = None

class HttpLog(HttpLogBase):
    id: uuid.UUID
    timestamp: datetime

    class Config:
        from_attributes = True

# Schema para validação de acesso RFID
class RFIDAccessRequest(BaseModel):
    card_id: str
    location: str

# NOVO SCHEMA PARA SINCRONIZAÇÃO
class UserSync(BaseModel):
    full_name: str
    has_time_restriction: bool
    time_window_start: str
    time_window_end: str

    class Config:
        from_attributes = True
        
class RFIDCredentialSync(BaseModel):
    card_id: str
    is_active: bool
    user: UserSync # Inclui as restrições do usuário

    class Config:
        from_attributes = True
