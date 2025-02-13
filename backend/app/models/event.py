from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class Event(BaseModel):
    __tablename__ = "events"

    event_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    description = Column(String)
    event_metadata = Column(JSON)
    
    # Foreign Keys
    user_id = Column(String(36), ForeignKey("users.id"))
    agent_id = Column(String(36), ForeignKey("agents.id"))
    
    # Relationships
    user = relationship("User", back_populates="events")
    agent = relationship("Agent", back_populates="events") 