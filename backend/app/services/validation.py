from typing import Dict, Any, List
from pydantic import ValidationError
from ..schemas.schemas import SecurityEvent, ThreatIndicator, NetworkTraffic
import logging

logger = logging.getLogger(__name__)

class DataValidationPipeline:
    def __init__(self):
        self.validators = {
            "security_event": self._validate_security_event,
            "threat_indicator": self._validate_threat_indicator,
            "network_traffic": self._validate_network_traffic
        }
        
    async def validate_input(self, data: Dict[str, Any], data_type: str) -> bool:
        try:
            return await self.validators[data_type](data)
        except ValidationError as e:
            logger.error(f"Validation error for {data_type}: {str(e)}")
            return False
            
    async def _validate_security_event(self, data: Dict[str, Any]) -> bool:
        """Validate security event data"""
        try:
            SecurityEvent(**data)
            return True
        except ValidationError as e:
            logger.error(f"Invalid security event: {str(e)}")
            return False
            
    async def _validate_threat_indicator(self, data: Dict[str, Any]) -> bool:
        """Validate threat indicator data"""
        try:
            ThreatIndicator(**data)
            return True
        except ValidationError as e:
            logger.error(f"Invalid threat indicator: {str(e)}")
            return False
            
    async def _validate_network_traffic(self, data: Dict[str, Any]) -> bool:
        """Validate network traffic data"""
        try:
            NetworkTraffic(**data)
            return True
        except ValidationError as e:
            logger.error(f"Invalid network traffic: {str(e)}")
            return False