from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str
    is_active: bool = True
    settings: Optional[Dict[str, Any]] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(OrganizationBase):
    pass

class OrganizationInDBBase(OrganizationBase):
    id: str
    api_key: str
    created_at: datetime

    class Config:
        from_attributes = True

class Organization(OrganizationInDBBase):
    pass 