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
        # Create tables if they don't exist
        if not create_tables(db):
            raise Exception("Failed to create database tables")
            
        # Check if we should create first superuser and their organization
        user = db.query(User).filter(User.email == settings.first_superuser).first()
        if not user and settings.first_superuser and settings.first_superuser_password:
            print("Creating first superuser and organization...")
            
            try:
                # Create default organization
                default_org = Organization(
                    name="Default Organization",
                    api_key=secrets.token_urlsafe(32),
                    is_active=True
                )
                db.add(default_org)
                db.flush()
                
                # Create superuser
                user = User(
                    email=settings.first_superuser,
                    hashed_password=get_password_hash(settings.first_superuser_password),
                    full_name="Default Admin",
                    is_superuser=True,
                    organization_id=default_org.id
                )
                db.add(user)
                db.commit()
                print(f"Created superuser {user.email} with organization {default_org.name}")
                
            except IntegrityError as e:
                print(f"Integrity Error while creating initial data: {str(e)}")
                db.rollback()
            except Exception as e:
                print(f"Error creating initial data: {str(e)}")
                db.rollback()
                
    except Exception as e:
        print(f"Database initialization error: {str(e)}")
        db.rollback()
        raise