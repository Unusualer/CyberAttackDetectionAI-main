from typing import Dict, Any, List
import psutil
import os
import asyncio
from datetime import datetime
import aioredis
from ..schemas.schemas import SystemHealth, ServiceStatus, ResourceMetrics
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class HealthMonitorService:
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL)
        self.critical_services = [
            "ml_engine",
            "threat_analyzer",
            "incident_response",
            "monitoring"
        ]
        self.resource_thresholds = {
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "disk_percent": 90.0
        }
        
    async def check_system_health(self) -> SystemHealth:
        """Check overall system health"""
        try:
            # Run all health checks concurrently
            cpu_health, memory_health, disk_health = await asyncio.gather(
                self._check_cpu_health(),
                self._check_memory_health(),
                self._check_disk_health()
            )
            
            # Check service status
            service_status = await self._check_services()
            
            # Check ML model health
            model_health = await self._check_model_health()
            
            # Determine overall system status
            overall_status = self._determine_overall_status(
                cpu_health,
                memory_health,
                disk_health,
                service_status,
                model_health
            )
            
            return SystemHealth(
                status=overall_status,
                timestamp=datetime.utcnow(),
                resources={
                    "cpu": cpu_health,
                    "memory": memory_health,
                    "disk": disk_health
                },
                services=service_status,
                models=model_health,
                warnings=self._generate_health_warnings(
                    cpu_health,
                    memory_health,
                    disk_health,
                    service_status,
                    model_health
                )
            )
            
        except Exception as e:
            logger.error(f"Error checking system health: {str(e)}")
            raise
            
    async def _check_cpu_health(self) -> ResourceMetrics:
        """Check CPU health metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_times = psutil.cpu_times()
            
            return ResourceMetrics(
                usage_percent=cpu_percent,
                status=self._get_resource_status(cpu_percent, "cpu_percent"),
                details={
                    "user": cpu_times.user,
                    "system": cpu_times.system,
                    "idle": cpu_times.idle,
                    "cores": psutil.cpu_count(),
                    "load_average": os.getloadavg()
                }
            )
        except Exception as e:
            logger.error(f"Error checking CPU health: {str(e)}")
            raise
            
    async def _check_memory_health(self) -> ResourceMetrics:
        """Check memory health metrics"""
        try:
            memory = psutil.virtual_memory()
            
            return ResourceMetrics(
                usage_percent=memory.percent,
                status=self._get_resource_status(memory.percent, "memory_percent"),
                details={
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "free": memory.free,
                    "swap_used": psutil.swap_memory().used
                }
            )
        except Exception as e:
            logger.error(f"Error checking memory health: {str(e)}")
            raise
            
    async def _check_services(self) -> Dict[str, ServiceStatus]:
        """Check status of critical services"""
        service_status = {}
        
        for service in self.critical_services:
            try:
                # Check if service is responding
                is_alive = await self._ping_service(service)
                
                # Get service metrics
                metrics = await self._get_service_metrics(service)
                
                service_status[service] = ServiceStatus(
                    status="healthy" if is_alive else "down",
                    last_check=datetime.utcnow(),
                    uptime=await self._get_service_uptime(service),
                    metrics=metrics
                )
                
            except Exception as e:
                logger.error(f"Error checking service {service}: {str(e)}")
                service_status[service] = ServiceStatus(
                    status="error",
                    last_check=datetime.utcnow(),
                    error=str(e)
                )
                
        return service_status
        
    async def _check_model_health(self) -> Dict[str, Any]:
        """Check ML model health metrics"""
        try:
            return {
                "anomaly_detector": await self._check_model_metrics("anomaly_detector"),
                "threat_classifier": await self._check_model_metrics("threat_classifier"),
                "behavior_analyzer": await self._check_model_metrics("behavior_analyzer")
            }
        except Exception as e:
            logger.error(f"Error checking model health: {str(e)}")
            raise
            
    def _determine_overall_status(
        self,
        cpu_health: ResourceMetrics,
        memory_health: ResourceMetrics,
        disk_health: ResourceMetrics,
        service_status: Dict[str, ServiceStatus],
        model_health: Dict[str, Any]
    ) -> str:
        """Determine overall system health status"""
        # Check for critical service failures
        critical_services_healthy = all(
            status.status == "healthy"
            for status in service_status.values()
        )
        
        # Check resource usage
        resources_healthy = all(
            metric.status == "healthy"
            for metric in [cpu_health, memory_health, disk_health]
        )
        
        # Check model health
        models_healthy = all(
            health["status"] == "healthy"
            for health in model_health.values()
        )
        
        if not critical_services_healthy:
            return "critical"
        elif not resources_healthy:
            return "warning"
        elif not models_healthy:
            return "degraded"
        else:
            return "healthy" 