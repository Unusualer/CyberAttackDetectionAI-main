from typing import Dict, Any, List
import aiohttp
from datetime import datetime
import json
from ...core.config import settings
import logging

logger = logging.getLogger(__name__)

class SIEMIntegration:
    def __init__(self):
        self.siem_url = settings.SIEM_URL
        self.api_key = settings.SIEM_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    async def send_event(self, event: Dict[str, Any]):
        """Send event to SIEM system"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.siem_url}/events",
                    headers=self.headers,
                    json=self._format_event(event)
                ) as response:
                    if response.status not in (200, 201):
                        logger.error(
                            f"Failed to send event to SIEM: {await response.text()}"
                        )
                    return await response.json()
                    
        except Exception as e:
            logger.error(f"Error sending event to SIEM: {str(e)}")
            raise
            
    def _format_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Format event for SIEM system"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "source": "cyber_defense_system",
            "event_type": event.get("type", "security_event"),
            "severity": event.get("severity", "medium"),
            "details": event,
            "metadata": {
                "version": settings.VERSION,
                "environment": settings.ENVIRONMENT
            }
        } 