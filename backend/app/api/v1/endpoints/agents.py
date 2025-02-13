from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import secrets

from app.api import deps
from app import schemas
from app.models.agent import Agent
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=schemas.Agent)
async def register_agent(
    *,
    db: Session = Depends(deps.get_db_sync),
    agent_in: schemas.AgentCreate,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """Register a new agent"""
    # Check if user belongs to the organization
    if current_user.organization_id != agent_in.organization_id:
        raise HTTPException(
            status_code=400,
            detail="User does not belong to the specified organization"
        )
    
    # Create agent with API key
    agent = Agent(
        name=agent_in.name,
        agent_type=agent_in.agent_type,
        organization_id=agent_in.organization_id,
        user_id=current_user.id,
        api_key=secrets.token_urlsafe(32)
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.get("/", response_model=List[schemas.Agent])
async def get_agents(
    db: Session = Depends(deps.get_db_sync),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """Retrieve agents"""
    # If user is superuser, return all agents
    if current_user.is_superuser:
        agents = db.query(Agent).offset(skip).limit(limit).all()
    else:
        # Otherwise, return only agents from user's organization
        agents = (
            db.query(Agent)
            .filter(Agent.organization_id == current_user.organization_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    return agents

@router.get("/{agent_id}", response_model=schemas.Agent)
async def get_agent(
    *,
    db: Session = Depends(deps.get_db_sync),
    agent_id: int,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """Get agent by ID"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check permissions
    if not current_user.is_superuser and agent.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return agent

@router.put("/{agent_id}", response_model=schemas.Agent)
async def update_agent(
    *,
    db: Session = Depends(deps.get_db_sync),
    agent_id: int,
    agent_in: schemas.AgentUpdate,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """Update agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check permissions
    if not current_user.is_superuser and agent.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Update attributes
    for field, value in agent_in.dict(exclude_unset=True).items():
        setattr(agent, field, value)
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.delete("/{agent_id}", response_model=schemas.Agent)
async def delete_agent(
    *,
    db: Session = Depends(deps.get_db_sync),
    agent_id: int,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """Delete agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check permissions
    if not current_user.is_superuser and agent.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(agent)
    db.commit()
    return agent