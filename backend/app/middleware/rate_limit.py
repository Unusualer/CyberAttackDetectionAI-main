from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
import time
from ..core.config import settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = {}
        self.window = 60  # 1 minute window
        
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old requests
        self.requests = {
            ip: times for ip, times in self.requests.items()
            if current_time - times[-1] < self.window
        }
        
        # Check rate limit
        if client_ip in self.requests:
            if len(self.requests[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
                raise HTTPException(status_code=429, detail="Too many requests")
            self.requests[client_ip].append(current_time)
        else:
            self.requests[client_ip] = [current_time]
            
        response = await call_next(request)
        return response 