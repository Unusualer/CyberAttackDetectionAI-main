from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from sqlalchemy.orm import Session
from app.api import deps
from app.services.ml.threat_detector import ThreatDetector
from app.models.models import SecurityEvent
from datetime import datetime

router = APIRouter()
threat_detector = ThreatDetector()

@router.post("/analyze", response_model=Dict)
def analyze_security_event(
    event_data: Dict,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    Analyze a security event for potential threats using both Keras and Isolation Forest models
    """
    try:
        # Run threat detection
        threat_analysis = threat_detector.detect_threats(event_data)
        
        # Create security event record
        security_event = SecurityEvent(
            agent_id=event_data.get("agent_id"),
            event_type=threat_analysis["attack_type"],
            severity=threat_analysis["severity"],
            description=f"Threat detected with {threat_analysis['confidence']:.2f} confidence",
            raw_data=event_data,
            timestamp=datetime.utcnow(),
            is_resolved=False
        )
        
        # Save to database
        db.add(security_event)
        db.commit()
        db.refresh(security_event)
        
        return {
            "event_id": security_event.id,
            "analysis": threat_analysis
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing security event: {str(e)}"
        )

@router.get("/events", response_model=Dict)
def get_security_events(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    Get list of security events with their threat analysis
    """
    try:
        events = db.query(SecurityEvent)\
            .order_by(SecurityEvent.timestamp.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
            
        return {
            "total": len(events),
            "events": [
                {
                    "id": event.id,
                    "timestamp": event.timestamp,
                    "event_type": event.event_type,
                    "severity": event.severity,
                    "description": event.description,
                    "is_resolved": event.is_resolved
                }
                for event in events
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching security events: {str(e)}"
        ) 