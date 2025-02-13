from fastapi import Request
import logging
import time
import json
from typing import Callable
from ..core.config import settings

logger = logging.getLogger("api")

class RequestLoggingMiddleware:
    async def __call__(
        self,
        request: Request,
        call_next: Callable
    ):
        # Start timer
        start_time = time.time()
        
        # Get request body
        body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.json()
            except:
                body = await request.body()

        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log request details
        log_dict = {
            "method": request.method,
            "path": request.url.path,
            "duration": f"{duration:.3f}s",
            "status_code": response.status_code,
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent"),
        }

        if body and settings.LOG_REQUEST_BODY:
            log_dict["body"] = body

        logger.info("API Request", extra=log_dict)
        
        return response 