from sqlalchemy import Boolean, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    organization_id = Column(String(36), ForeignKey("organizations.id"), nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="users")
    events = relationship("Event", back_populates="user")
    agents = relationship("Agent", back_populates="user") 