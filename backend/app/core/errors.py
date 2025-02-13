from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging
from .logging import setup_logging
import traceback
import uuid
logger = logging.getLogger(__name__)
def generate_error_id() -> str:
    """Generate a unique error ID"""
    return str(uuid.uuid4())

class AppError(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None,
        error_type: str = None,
        metadata: Dict[str, Any] = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.error_type = error_type
        self.metadata = metadata or {}

class SecurityError(AppError):
    """Security-related errors"""
    def __init__(self, detail: str, error_code: str = None, metadata: Dict[str, Any] = None):
        super().__init__(
            status_code=403,
            detail=detail,
            error_code=error_code or "SECURITY_ERROR",
            error_type="security",
            metadata=metadata
        )

class MLError(AppError):
    """ML-related errors"""
    def __init__(self, detail: str, error_code: str = None, metadata: Dict[str, Any] = None):
        super().__init__(
            status_code=500,
            detail=detail,
            error_code=error_code or "ML_ERROR",
            error_type="ml",
            metadata=metadata
        )

async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global error handler"""
    error_id = generate_error_id()
    
    if isinstance(exc, AppError):
        log_error(
            error_id,
            exc.detail,
            exc.error_type,
            exc.error_code,
            exc.metadata,
            request
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_id": error_id,
                "detail": exc.detail,
                "error_code": exc.error_code,
                "type": exc.error_type
            }
        )
    
    # Unexpected errors
    log_error(
        error_id,
        str(exc),
        "system",
        "INTERNAL_ERROR",
        {"traceback": traceback.format_exc()},
        request
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error_id": error_id,
            "detail": "An unexpected error occurred",
            "error_code": "INTERNAL_ERROR",
            "type": "system"
        }
    )

def log_error(
    error_id: str,
    message: str,
    error_type: str,
    error_code: str,
    metadata: Dict[str, Any],
    request: Request
) -> None:
    """Log error details"""
    logger.error(
        f"Error {error_id}: {message}",
        extra={
            "error_id": error_id,
            "error_type": error_type,
            "error_code": error_code,
            "metadata": metadata,
            "request": {
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host,
                "headers": dict(request.headers)
            }
        }
    ) 