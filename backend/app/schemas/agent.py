from typing import Optional
from pydantic import BaseModel

class AgentBase(BaseModel):
    name: Optional[str] = None
    agent_type: str
    status: Optional[str] = "active"
    is_active: Optional[bool] = True
    configuration: Optional[str] = None
    organization_id: Optional[int] = None
    user_id: Optional[int] = None

class AgentCreate(AgentBase):
    agent_type: str
    organization_id: int

class AgentUpdate(AgentBase):
    pass

class AgentInDBBase(AgentBase):
    id: int
    api_key: str
    last_heartbeat: Optional[str] = None

    class Config:
        from_attributes = True

class Agent(AgentInDBBase):
    pass

class AgentInDB(AgentInDBBase):
    pass 