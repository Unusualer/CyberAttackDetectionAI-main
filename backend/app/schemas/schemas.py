from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class EventSeverity(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPROMISED = "compromised"

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str
    organization_id: str

class User(UserBase):
    id: str
    is_superuser: bool = False
    organization_id: str

    class Config:
        from_attributes = True

# Organization schemas
class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    admin_email: EmailStr
    admin_password: str

class Organization(OrganizationBase):
    id: str
    api_key: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Security Event schemas
class SecurityEventCreate(BaseModel):
    event_type: str
    severity: EventSeverity
    description: str
    raw_data: dict

class SecurityEvent(SecurityEventCreate):
    id: str
    agent_id: str
    timestamp: datetime
    is_resolved: bool

    class Config:
        from_attributes = True 