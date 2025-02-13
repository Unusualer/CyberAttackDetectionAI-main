from enum import Enum
from typing import Optional
from fastapi import Header, HTTPException

class APIVersion(str, Enum):
    V1 = "v1"
    V2 = "v2"
    LATEST = "v2"

def get_api_version(
    api_version: Optional[str] = Header(None, alias="X-API-Version")
) -> APIVersion:
    """Get and validate API version"""
    if api_version is None:
        return APIVersion.LATEST
        
    try:
        return APIVersion(api_version.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid API version. Supported versions: {[v.value for v in APIVersion]}"
        ) 