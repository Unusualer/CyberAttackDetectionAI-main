from typing import Dict, Any
import psutil
import time
from datetime import datetime
import asyncio
from ..core.config import settings
from prometheus_client import Gauge, Histogram
import logging

logger = logging.getLogger(__name__)

# Prometheus metrics
RESPONSE_TIME = Histogram(
    'api_response_time_seconds',
    'API endpoint response time',
    ['endpoint', 'method']
)

SYSTEM_MEMORY = Gauge(
    'system_memory_usage_bytes',
    'System memory usage in bytes'
)

SYSTEM_CPU = Gauge(
    'system_cpu_usage_percent',
    'System CPU usage percentage'
)

class PerformanceMonitor:
    def __init__(self):
        self.thresholds = {
            'cpu_percent': settings.CPU_THRESHOLD,
            'memory_percent': settings.MEMORY_THRESHOLD,
            'response_time': settings.RESPONSE_TIME_THRESHOLD
        }
        
    async def monitor_system_resources(self):
        """Monitor system resources continuously"""
        while True:
            try:
                # Collect metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                # Update Prometheus metrics
                SYSTEM_CPU.set(cpu_percent)
                SYSTEM_MEMORY.set(memory.used)
                
                # Check thresholds
                if cpu_percent > self.thresholds['cpu_percent']:
                    logger.warning(f"High CPU usage: {cpu_percent}%")
                    
                if memory.percent > self.thresholds['memory_percent']:
                    logger.warning(f"High memory usage: {memory.percent}%")
                    
                await asyncio.sleep(settings.MONITORING_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error monitoring system resources: {str(e)}")
                await asyncio.sleep(5)
                
    def track_response_time(self, endpoint: str, method: str):
        """Decorator to track endpoint response time"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Record metric
                RESPONSE_TIME.labels(
                    endpoint=endpoint,
                    method=method
                ).observe(duration)
                
                # Check threshold
                if duration > self.thresholds['response_time']:
                    logger.warning(
                        f"Slow response from {method} {endpoint}: {duration:.2f}s"
                    )
                    
                return result
            return wrapper
        return decorator 