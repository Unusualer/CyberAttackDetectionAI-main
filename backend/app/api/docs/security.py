SECURITY_RESPONSES = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Could not validate credentials"
                }
            }
        }
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Insufficient permissions"
                }
            }
        }
    }
}

THREAT_DETECTION_DOCS = {
    "summary": "Detect threats in real-time",
    "description": """
    Analyzes incoming traffic and events for potential security threats using AI/ML models.
    Supports detection of:
    - Anomalous behavior
    - Known attack patterns
    - Zero-day exploits
    - Data exfiltration attempts
    """,
    "responses": {
        200: {
            "description": "Successful threat analysis",
            "content": {
                "application/json": {
                    "example": {
                        "threat_detected": True,
                        "severity": "high",
                        "confidence": 0.95,
                        "details": {
                            "type": "anomaly",
                            "indicators": ["unusual_traffic_pattern", "suspicious_ip"]
                        }
                    }
                }
            }
        },
        **SECURITY_RESPONSES
    }
} 