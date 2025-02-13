from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.models import Organization, User
from ..schemas import schemas
from .base import BaseRepository

class OrganizationRepository(BaseRepository[Organization, schemas.OrganizationCreate, schemas.OrganizationUpdate]):
    def __init__(self):
        super().__init__(Organization)

    async def get_by_api_key(self, db: Session, api_key: str) -> Optional[Organization]:
        query = select(self.model).where(self.model.api_key == api_key)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_users(
        self,
        db: Session,
        *,
        org_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        query = select(User).where(
            User.organization_id == org_id
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_active_organizations(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Organization]:
        query = select(self.model).where(
            self.model.is_active == True
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all() 