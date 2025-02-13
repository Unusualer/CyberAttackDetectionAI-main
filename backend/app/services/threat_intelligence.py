from typing import Dict, Any, List
import aiohttp
import asyncio
from datetime import datetime, timedelta
from ..core.config import settings
from ..schemas.schemas import ThreatIndicator
import logging

logger = logging.getLogger(__name__)

class ThreatIntelligence:
    def __init__(self):
        self.api_key = settings.THREAT_INTEL_API_KEY
        self.cache_ttl = timedelta(minutes=30)
        self.indicators_cache = {}
        
    async def update_indicators(self):
        """Update threat indicators from various sources"""
        try:
            # Fetch from different sources concurrently
            results = await asyncio.gather(
                self._fetch_alienvault_indicators(),
                self._fetch_virustotal_indicators(),
                self._fetch_custom_indicators()
            )
            
            # Merge and deduplicate indicators
            all_indicators = []
            for source_indicators in results:
                all_indicators.extend(source_indicators)
                
            # Update cache
            self.indicators_cache = {
                "last_updated": datetime.utcnow(),
                "indicators": all_indicators
            }
            
            logger.info(f"Updated {len(all_indicators)} threat indicators")
            return all_indicators
            
        except Exception as e:
            logger.error(f"Error updating threat indicators: {str(e)}")
            raise
            
    async def _fetch_alienvault_indicators(self) -> List[ThreatIndicator]:
        """Fetch indicators from AlienVault OTX"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.ALIENVAULT_API_URL}/indicators/recent",
                headers={"X-OTX-API-KEY": settings.ALIENVAULT_API_KEY}
            ) as response:
                data = await response.json()
                return self._parse_alienvault_indicators(data)
                
    async def _fetch_virustotal_indicators(self) -> List[ThreatIndicator]:
        """Fetch indicators from VirusTotal"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.VIRUSTOTAL_API_URL}/intelligence",
                headers={"x-apikey": settings.VIRUSTOTAL_API_KEY}
            ) as response:
                data = await response.json()
                return self._parse_virustotal_indicators(data)
                
    def _parse_alienvault_indicators(self, data: Dict) -> List[ThreatIndicator]:
        """Parse AlienVault indicators"""
        indicators = []
        for item in data.get("results", []):
            indicators.append(
                ThreatIndicator(
                    type=item["type"],
                    value=item["indicator"],
                    confidence=item["confidence"],
                    source="alienvault",
                    last_seen=datetime.fromisoformat(item["last_seen"])
                )
            )
        return indicators 