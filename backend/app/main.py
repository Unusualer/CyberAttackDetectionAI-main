from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql import text

from app.api.v1.api import api_router
from app.core.config import settings
from app.middleware.rate_limit import RateLimitMiddleware
from app.db.session import SessionLocal
from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize services
    print("Starting up...")
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    yield
    # Shutdown: Clean up resources
    print("Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
app.add_middleware(RateLimitMiddleware)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify system status
    """
    health_status = {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.environment,
        "database": "not_checked",
        "components": {
            "api": "healthy",
            "database": "not_checked",
            "redis": "not_checked"
        }
    }
    
    try:
        # Check database connection
        db = SessionLocal()
        try:
            # Try to execute a simple query
            db.execute(text("SELECT 1"))
            health_status["database"] = "healthy"
            health_status["components"]["database"] = "healthy"
        except Exception as e:
            health_status["database"] = f"unhealthy: {str(e)}"
            health_status["components"]["database"] = "unhealthy"
            health_status["status"] = "degraded"
        finally:
            db.close()
    except Exception as e:
        health_status["database"] = f"connection_failed: {str(e)}"
        health_status["components"]["database"] = "unavailable"
        health_status["status"] = "degraded"

    return health_status

@app.get("/")
async def root():
    return {
        "message": "Welcome to Cyber Defense API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    } 