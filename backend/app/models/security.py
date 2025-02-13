from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from ..db.base_class import Base

class ThreatIndicator(Base):
    __tablename__ = "threat_indicators"
    
    id = Column(String(36), primary_key=True)
    type = Column(String(50), nullable=False)
    value = Column(String(255), nullable=False)
    confidence = Column(Float, nullable=False)
    source = Column(String(50), nullable=False)
    last_seen = Column(DateTime, nullable=False)
    metadata = Column(JSON)

class SecurityAlert(Base):
    __tablename__ = "security_alerts"
    
    id = Column(String(36), primary_key=True)
    alert_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False)
    resolved_at = Column(DateTime)
    details = Column(JSON) 