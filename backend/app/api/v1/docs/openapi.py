from fastapi.openapi.utils import get_openapi

def custom_openapi():
    """Generate custom OpenAPI documentation"""
    openapi_schema = get_openapi(
        title="Cyber Defense API",
        version="1.0.0",
        description="AI-powered Cyber Attack Detection API",
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    return openapi_schema 