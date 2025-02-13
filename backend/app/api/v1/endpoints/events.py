from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ....schemas import schemas
from ....api import deps
from ....models import models
from ....services import ml_service, notification_service

router = APIRouter()

@router.post("/", response_model=schemas.SecurityEvent)
async def create_event(
    *,
    db: Session = Depends(deps.get_db),
    event_in: schemas.SecurityEventCreate,
    agent_id: str,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """Create new security event"""
    # Verify agent belongs to organization
    agent = db.query(models.Agent).filter(
        models.Agent.id == agent_id,
        models.Agent.organization_id == current_user.organization_id
    ).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Create event
    event = models.SecurityEvent(
        agent_id=agent_id,
        event_type=event_in.event_type,
        severity=event_in.severity,
        description=event_in.description,
        raw_data=event_in.raw_data
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    # Process event in background
    background_tasks.add_task(
        ml_service.analyze_event,
        event.id,
        current_user.organization_id
    )
    
    # Send notifications for high severity events
    if event.severity >= schemas.EventSeverity.HIGH:
        background_tasks.add_task(
            notification_service.send_alert,
            event.id,
            current_user.organization_id
        )

    return event

@router.get("/", response_model=List[schemas.SecurityEvent])
async def get_events(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """Get all security events for organization"""
    events = db.query(models.SecurityEvent).join(
        models.Agent
    ).filter(
        models.Agent.organization_id == current_user.organization_id
    ).order_by(
        models.SecurityEvent.timestamp.desc()
    ).offset(skip).limit(limit).all()
    return events 