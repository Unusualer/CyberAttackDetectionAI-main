from typing import Dict, Any
import psutil
import asyncio
from datetime import datetime
from ..core.config import settings
from .ml.training_pipeline import ModelTrainingPipeline
from .monitoring import MonitoringService

class HealthCheckService:
    def __init__(self):
        self.model_pipeline = ModelTrainingPipeline()
        self.monitoring = MonitoringService()

    async def check_all(self) -> Dict[str, Any]:
        """Run all health checks"""
        return {
            "status": "healthy",  # or "degraded", "unhealthy"
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "system": await self._check_system_health(),
                "ml_models": await self._check_ml_health(),
                "database": await self._check_database(),
                "cache": await self._check_cache(),
                "monitoring": await self._check_monitoring()
            }
        }

    async def _check_system_health(self) -> Dict[str, Any]:
        """Check system resources"""
        return {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "status": "healthy"
        }

    async def _check_ml_health(self) -> Dict[str, Any]:
        """Check ML models health"""
        model_metrics = await self.model_pipeline.get_model_metrics()
        return {
            "models_loaded": len(model_metrics) > 0,
            "accuracy_metrics": model_metrics,
            "last_training": self.model_pipeline.last_training_time,
            "status": "healthy" if model_metrics["accuracy"] > 0.9 else "degraded"
        } 