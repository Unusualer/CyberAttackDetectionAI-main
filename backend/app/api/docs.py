from fastapi.openapi.utils import get_openapi
from ..core.config import settings

def custom_openapi():
    """Generate custom OpenAPI schema"""
    
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="AI-powered Cyber Attack Detection API",
        version=settings.VERSION,
        description="""
        AI-powered Cyber Attack Detection System API
        
        Features:
        - Real-time threat detection using ML/AI
        - Anomaly detection and behavioral analysis
        - Automated incident response
        - Threat hunting capabilities
        - Advanced security analytics
        
        Authentication:
        - JWT Bearer token required for all endpoints
        - Organization-based access control
        
        ## Rate Limiting
        API requests are limited to:
        - 60 requests/minute for standard endpoints
        - 10 requests/minute for ML inference endpoints
        
        ## Error Codes
        - 400: Bad Request - Invalid input
        - 401: Unauthorized - Missing or invalid token
        - 403: Forbidden - Insufficient permissions
        - 404: Not Found - Resource doesn't exist
        - 429: Too Many Requests - Rate limit exceeded
        - 500: Internal Server Error - Server-side error
        """,
        routes=app.routes,
    )

    # Security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Add example responses
    openapi_schema["components"]["examples"] = {
        "ThreatDetection": {
            "value": {
                "event_id": "evt_123",
                "threat_detected": True,
                "threat_type": "anomaly",
                "severity": "high",
                "confidence": 0.95,
                "details": {
                    "indicators": ["unusual_traffic", "suspicious_process"],
                    "affected_system": "192.168.1.100",
                    "timestamp": "2024-01-20T10:30:00Z"
                }
            }
        },
        "SecurityAlert": {
            "value": {
                "alert_id": "alt_456",
                "type": "intrusion_attempt",
                "severity": "critical",
                "source_ip": "10.0.0.5",
                "timestamp": "2024-01-20T10:35:00Z",
                "details": {
                    "attack_vector": "sql_injection",
                    "target_endpoint": "/api/users",
                    "request_count": 150
                }
            }
        }
    }

    # Add tags metadata
    openapi_schema["tags"] = [
        {
            "name": "Security",
            "description": "Threat detection and response endpoints"
        },
        {
            "name": "Monitoring",
            "description": "System monitoring and metrics"
        },
        {
            "name": "Analytics",
            "description": "Security analytics and reporting"
        },
        {
            "name": "Management",
            "description": "System configuration and management"
        }
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Update main.py to use custom OpenAPI schema
app.openapi = custom_openapi