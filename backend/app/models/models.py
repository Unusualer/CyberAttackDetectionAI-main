from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.base_class import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    agents = relationship("Agent", back_populates="organization")
    users = relationship("User", back_populates="organization")

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    organization_id = Column(String, ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="users")

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, default=generate_uuid)
    hostname = Column(String, nullable=False)
    ip_address = Column(String)
    status = Column(String, default="active")
    last_seen = Column(DateTime, default=datetime.utcnow)
    version = Column(String)
    organization_id = Column(String, ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="agents")
    events = relationship("SecurityEvent", back_populates="agent")

class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, ForeignKey("agents.id"))
    event_type = Column(String, nullable=False)
    severity = Column(Integer)
    description = Column(String)
    raw_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_resolved = Column(Boolean, default=False)

    agent = relationship("Agent", back_populates="events") 