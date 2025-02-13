from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class Agent(BaseModel):
    __tablename__ = "agents"

    name = Column(String, index=True)
    agent_type = Column(String, nullable=False)
    status = Column(String, default="active")
    api_key = Column(String(64), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    last_heartbeat = Column(String, nullable=True)
    configuration = Column(String, nullable=True)
    
    # Foreign Keys
    organization_id = Column(String(36), ForeignKey("organizations.id"))
    user_id = Column(String(36), ForeignKey("users.id"))

    # Relationships
    organization = relationship("Organization", back_populates="agents")
    user = relationship("User", back_populates="agents")
    events = relationship("Event", back_populates="agent") 