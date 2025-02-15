from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.sql import text
from app.core.config import settings
from app.models.base import Base
from app.models.user import User
from app.core.security import get_password_hash
from app.models.organization import Organization
import secrets
import time
from datetime import datetime

def wait_for_db(db: Session, max_retries: int = 30, retry_interval: int = 1) -> bool:
    """Wait for database to be ready"""
    for _ in range(max_retries):
        try:
            # Try a simple query
            db.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Waiting for database... {str(e)}")
            time.sleep(retry_interval)
    return False

def create_tables(db: Session) -> bool:
    """Create database tables if they don't exist"""
    try:
        # Check if tables exist by trying to query the users table
        db.execute(text("SELECT 1 FROM users LIMIT 1"))
        print("Tables already exist")
        return True
    except Exception:
        try:
            # Tables don't exist, create them
            Base.metadata.create_all(bind=db.get_bind())
            print("Created all database tables successfully")
            return True
        except Exception as e:
            print(f"Error creating tables: {str(e)}")
            return False

def init_db(db: Session) -> None:
    """Initialize database with required tables and initial data"""
    
    # Wait for database to be ready
    if not wait_for_db(db):
        raise Exception("Database not available after maximum retries")
        
    try:
        print("Initializing database with initial data...")
        # Create default organization if it doesn't exist
        organization = db.query(Organization).first()
        if not organization:
            print("Creating default organization...")
            organization = Organization(
                name="Default Organization",
                api_key=settings.default_api_key,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(organization)
            db.commit()
            db.refresh(organization)
            print("Default organization created successfully")

        # Create superuser if it doesn't exist
        user = db.query(User).filter(User.email == settings.first_superuser).first()
        if not user:
            print("Creating superuser...")
            user = User(
                email=settings.first_superuser,
                hashed_password=get_password_hash(settings.first_superuser_password),
                full_name="Initial Super User",
                is_superuser=True,
                is_active=True,
                organization_id=organization.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print("Superuser created successfully")

    except Exception as e:
        db.rollback()
        print(f"Error in init_db: {str(e)}")
        raise e