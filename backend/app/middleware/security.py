from fastapi import Request, Response
from typing import Callable
import re
import logging

logger = logging.getLogger(__name__)

class SecurityMiddleware:
    def __init__(
        self,
        app,
        allowed_hosts: list = None,
        enable_xss_protection: bool = True,
        enable_hsts: bool = True
    ):
        self.app = app
        self.allowed_hosts = allowed_hosts or []
        self.enable_xss_protection = enable_xss_protection
        self.enable_hsts = enable_hsts
        
        # Compile regex patterns for input validation
        self.sql_injection_pattern = re.compile(
            r"(?i)(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|--)"
        )
        self.xss_pattern = re.compile(
            r"(?i)<script|javascript:|data:|vbscript:|<img|<iframe"
        )

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        # Host validation
        if self.allowed_hosts:
            host = request.headers.get("host", "").split(":")[0]
            if host not in self.allowed_hosts:
                return Response(
                    content="Invalid host header",
                    status_code=400
                )

        # Input validation
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.json()
                if self._contains_malicious_input(body):
                    logger.warning(f"Malicious input detected from {request.client.host}")
                    return Response(
                        content="Invalid input detected",
                        status_code=400
                    )
            except:
                pass

        response = await call_next(request)

        # Security headers
        if self.enable_xss_protection:
            response.headers["X-XSS-Protection"] = "1; mode=block"
        
        if self.enable_hsts:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response

    def _contains_malicious_input(self, data: dict) -> bool:
        """Check for potentially malicious input"""
        def check_value(value):
            if isinstance(value, str):
                if self.sql_injection_pattern.search(value):
                    return True
                if self.xss_pattern.search(value):
                    return True
            elif isinstance(value, dict):
                return any(check_value(v) for v in value.values())
            elif isinstance(value, list):
                return any(check_value(v) for v in value)
            return False

        return check_value(data) 