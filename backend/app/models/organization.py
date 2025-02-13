from sqlalchemy import Column, String, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .base import BaseModel

def generate_uuid():
    return str(uuid.uuid4())

class Organization(BaseModel):
    __tablename__ = "organizations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    api_key = Column(String(64), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    settings = Column(JSON, nullable=True)

    # Relationships
    users = relationship("User", back_populates="organization")
    agents = relationship("Agent", back_populates="organization") 