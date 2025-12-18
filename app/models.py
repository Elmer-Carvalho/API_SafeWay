from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.database import Base

class EventType(str, enum.Enum):
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"
    CARD_NOT_FOUND = "card_not_found"

class ErrorSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamento com credenciais RFID
    rfid_credentials = relationship("RFIDCredential", back_populates="user")

class RFIDCredential(Base):
    __tablename__ = "rfid_credentials"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    card_id = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Campos de restrição de horário
    has_time_restriction = Column(Boolean, default=False)
    time_window_start = Column(String(5), nullable=True)  # Formato "HH:MM"
    time_window_end = Column(String(5), nullable=True)    # Formato "HH:MM"
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    user = relationship("User", back_populates="rfid_credentials")
    access_logs = relationship("AccessLog", back_populates="rfid_credential")

class AccessLog(Base):
    __tablename__ = "access_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  
    rfid_credential_id = Column(UUID(as_uuid=True), ForeignKey("rfid_credentials.id"), nullable=True)  
    event_type = Column(Enum(EventType), nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    user = relationship("User")
    rfid_credential = relationship("RFIDCredential", back_populates="access_logs")


class ErrorLog(Base):
    __tablename__ = "error_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    error_type = Column(String(255), nullable=False)
    component = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(ErrorSeverity), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class HttpLog(Base):
    __tablename__ = "http_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    method = Column(String(10), nullable=False)
    endpoint = Column(String(255), nullable=False)
    status_code = Column(Integer, nullable=False)
    payload = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

