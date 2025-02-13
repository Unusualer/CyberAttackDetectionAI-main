from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.user import User as UserSchema

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def get_current_user(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.get("/", response_model=List[UserSchema])
def get_users(
    db: Session = Depends(deps.get_db_sync),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Retrieve users. Only accessible by superusers.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserSchema)
def get_user(
    *,
    db: Session = Depends(deps.get_db_sync),
    user_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get user by ID. Only accessible by superusers or the user themselves.
    """
    if current_user.id == user_id or current_user.is_superuser:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    raise HTTPException(
        status_code=403,
        detail="Not enough permissions to access this user's information"
    ) 