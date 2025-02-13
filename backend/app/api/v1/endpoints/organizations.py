from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import secrets

from app.api import deps
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, Organization as OrganizationSchema

router = APIRouter()

def generate_api_key() -> str:
    return secrets.token_urlsafe(32)

@router.post("/", response_model=OrganizationSchema)
def create_organization(
    request: Request,
    *,
    db: Session = Depends(deps.get_db_sync),
    organization_in: OrganizationCreate
) -> Any:
    """
    Create new organization.
    """
    # Create organization with API key
    organization = Organization(
        name=organization_in.name,
        api_key=generate_api_key(),
        is_active=organization_in.is_active,
        settings=organization_in.settings
    )
    db.add(organization)
    try:
        db.commit()
        db.refresh(organization)
        return organization
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Could not create organization: {str(e)}"
        )

@router.get("/", response_model=List[OrganizationSchema])
def get_organizations(
    db: Session = Depends(deps.get_db_sync),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Retrieve organizations.
    """
    if current_user.is_superuser:
        organizations = db.query(Organization).offset(skip).limit(limit).all()
    else:
        organizations = [current_user.organization]
    return organizations

@router.get("/{organization_id}", response_model=OrganizationSchema)
def get_organization(
    *,
    db: Session = Depends(deps.get_db_sync),
    organization_id: str,
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get organization by ID.
    """
    organization = db.query(Organization).filter(Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    if not current_user.is_superuser and current_user.organization_id != organization.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return organization 