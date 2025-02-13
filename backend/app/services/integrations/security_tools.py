from typing import Dict, Any, List
import aiohttp
import asyncio
from ...core.config import settings
import logging

logger = logging.getLogger(__name__)

class SecurityToolsIntegration:
    def __init__(self):
        self.tools_config = settings.SECURITY_TOOLS
        self.integrations = {
            "firewall": self._update_firewall,
            "ids": self._update_ids,
            "waf": self._update_waf
        }
        
    async def update_security_tools(self, updates: Dict[str, List[Dict[str, Any]]]):
        """Update multiple security tools"""
        tasks = []
        for tool_type, rules in updates.items():
            if tool_type in self.integrations:
                tasks.append(self.integrations[tool_type](rules))
                
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return self._process_results(results)
        
    async def _update_firewall(self, rules: List[Dict[str, Any]]):
        """Update firewall rules"""
        config = self.tools_config["firewall"]
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{config['url']}/rules/batch",
                    headers={"Authorization": f"Bearer {config['api_key']}"},
                    json={"rules": rules}
                ) as response:
                    return await response.json()
        except Exception as e:
            logger.error(f"Error updating firewall rules: {str(e)}")
            raise
            
    async def _update_ids(self, rules: List[Dict[str, Any]]):
        """Update IDS rules"""
        config = self.tools_config["ids"]
        try:
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    f"{config['url']}/rules",
                    headers={"X-API-Key": config['api_key']},
                    json={"rules": rules}
                ) as response:
                    return await response.json()
        except Exception as e:
            logger.error(f"Error updating IDS rules: {str(e)}")
            raise 