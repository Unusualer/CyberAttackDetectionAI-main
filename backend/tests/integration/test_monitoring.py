import pytest
from ...app.services.monitoring import MonitoringService
from ...app.services.health_monitor import HealthMonitorService

pytestmark = pytest.mark.asyncio

async def test_monitoring_system(test_db):
    """Test monitoring and health check system"""
    monitoring_service = MonitoringService()
    health_monitor = HealthMonitorService()

    # Test system health check
    health_status = await health_monitor.check_system_health()
    assert health_status.status in ["healthy", "warning", "critical", "degraded"]
    assert "cpu" in health_status.resources
    assert "memory" in health_status.resources
    assert "disk" in health_status.resources

    # Test real-time monitoring
    metrics = await monitoring_service.get_current_metrics("test_org")
    assert "network" in metrics
    assert "security" in metrics
    assert "system" in metrics

    # Test alert generation
    test_event = {
        "type": "high_cpu_usage",
        "severity": "warning",
        "details": {"cpu_usage": 90}
    }
    alert = await monitoring_service._generate_alert(
        "system_resource",
        test_event
    )
    assert alert["type"] == "system_resource"
    assert alert["severity"] == "warning" 