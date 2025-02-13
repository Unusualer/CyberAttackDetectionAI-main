from typing import Dict, Any, List, AsyncGenerator
import asyncio
from datetime import datetime
import aioredis
from ..schemas.schemas import MonitoringMetrics, SystemStatus, NetworkTraffic
from ..core.config import settings
from .threat_analysis import ThreatAnalysisService
import logging

logger = logging.getLogger(__name__)

class MonitoringService:
    def __init__(self):
        self.threat_analyzer = ThreatAnalysisService()
        self.redis = aioredis.from_url(settings.REDIS_URL)
        self.alert_channels = {}
        self.metrics_buffer = {}
        
    async def start_monitoring(self) -> None:
        """Start all monitoring tasks"""
        try:
            # Start monitoring tasks
            await asyncio.gather(
                self._monitor_network_traffic(),
                self._monitor_system_metrics(),
                self._monitor_security_events(),
                self._process_metrics_buffer()
            )
        except Exception as e:
            logger.error(f"Error starting monitoring: {str(e)}")
            raise

    async def subscribe_to_alerts(
        self,
        organization_id: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Subscribe to real-time alerts"""
        channel = await self.redis.subscribe(f"alerts:{organization_id}")
        try:
            while True:
                message = await channel.get_message(timeout=1.0)
                if message and message["type"] == "message":
                    yield message["data"]
        finally:
            await self.redis.unsubscribe(f"alerts:{organization_id}")

    async def get_current_metrics(self, organization_id: str) -> MonitoringMetrics:
        """Get current monitoring metrics"""
        try:
            metrics = await self.redis.get(f"metrics:{organization_id}")
            if not metrics:
                return MonitoringMetrics()
            return MonitoringMetrics.parse_raw(metrics)
        except Exception as e:
            logger.error(f"Error getting metrics: {str(e)}")
            raise

    async def _monitor_network_traffic(self) -> None:
        """Monitor network traffic in real-time"""
        while True:
            try:
                # Get network traffic data
                traffic = await self._collect_network_traffic()
                
                # Analyze for anomalies
                analysis = await self.threat_analyzer.analyze_traffic(traffic)
                
                # Update metrics
                await self._update_metrics("network", traffic)
                
                # Generate alerts if needed
                if analysis.threats_detected:
                    await self._generate_alert(
                        "network_threat",
                        analysis.details
                    )
                    
                await asyncio.sleep(settings.NETWORK_MONITORING_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in network monitoring: {str(e)}")
                await asyncio.sleep(5)  # Wait before retrying

    async def _monitor_system_metrics(self) -> None:
        """Monitor system performance metrics"""
        while True:
            try:
                # Collect system metrics
                metrics = await self._collect_system_metrics()
                
                # Check for resource issues
                if self._detect_resource_issues(metrics):
                    await self._generate_alert(
                        "system_resource",
                        metrics
                    )
                    
                # Update metrics buffer
                self._update_metrics_buffer("system", metrics)
                
                await asyncio.sleep(settings.SYSTEM_MONITORING_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in system monitoring: {str(e)}")
                await asyncio.sleep(5)

    async def _monitor_security_events(self) -> None:
        """Monitor security events in real-time"""
        while True:
            try:
                # Get security events
                events = await self._collect_security_events()
                
                # Process each event
                for event in events:
                    # Analyze event
                    analysis = await self.threat_analyzer.analyze_event(event)
                    
                    # Update metrics
                    await self._update_metrics("security", {
                        "event_type": event.type,
                        "severity": event.severity,
                        "timestamp": event.timestamp
                    })
                    
                    # Generate alert if threat detected
                    if analysis.risk_score > settings.ALERT_THRESHOLD:
                        await self._generate_alert(
                            "security_threat",
                            analysis.details
                        )
                        
                await asyncio.sleep(settings.SECURITY_MONITORING_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in security monitoring: {str(e)}")
                await asyncio.sleep(5)

    async def _generate_alert(
        self,
        alert_type: str,
        details: Dict[str, Any]
    ) -> None:
        """Generate and distribute alert"""
        alert = {
            "type": alert_type,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details
        }
        
        # Publish alert to Redis
        await self.redis.publish(
            f"alerts:{details['organization_id']}",
            alert
        )
        
        # Store alert in database
        await self._store_alert(alert)

    async def _update_metrics(
        self,
        metric_type: str,
        data: Dict[str, Any]
    ) -> None:
        """Update monitoring metrics"""
        try:
            metrics_key = f"metrics:{data['organization_id']}"
            current = await self.redis.get(metrics_key) or {}
            
            # Update metrics
            current[metric_type] = {
                "timestamp": datetime.utcnow().isoformat(),
                "data": data
            }
            
            # Store updated metrics
            await self.redis.set(
                metrics_key,
                current,
                ex=settings.METRICS_TTL
            )
            
        except Exception as e:
            logger.error(f"Error updating metrics: {str(e)}") 