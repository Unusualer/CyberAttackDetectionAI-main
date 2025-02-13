import pytest
from httpx import AsyncClient
from ...app.main import app
from ...app.core.config import settings

pytestmark = pytest.mark.asyncio

async def test_threat_detection_pipeline(
    client,
    test_db,
    test_threat_analyzer
):
    """Test complete threat detection pipeline"""
    # Test data
    test_event = {
        "source_ip": "192.168.1.100",
        "destination_ip": "10.0.0.2",
        "timestamp": "2023-11-22T10:00:00Z",
        "protocol": "TCP",
        "bytes_sent": 15000,
        "port": 445,
        "duration": 120,
        "packets": 150
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Submit event for analysis
        response = await ac.post(
            f"{settings.API_V1_STR}/threats/detect",
            json=test_event
        )
        assert response.status_code == 201
        result = response.json()

        # Verify threat analysis results
        assert "threat_detected" in result
        assert "severity" in result
        assert "confidence" in result
        assert "details" in result

        # If threat detected, verify incident response
        if result["threat_detected"]:
            incident_response = await ac.get(
                f"{settings.API_V1_STR}/incidents/{result['incident_id']}"
            )
            assert incident_response.status_code == 200
            incident = incident_response.json()
            assert incident["status"] in ["open", "investigating", "contained"] 