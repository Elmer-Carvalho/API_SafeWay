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

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

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
