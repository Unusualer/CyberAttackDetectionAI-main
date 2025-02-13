from typing import Dict, Any, List
import asyncio
from datetime import datetime, timedelta
import numpy as np
from ..schemas.schemas import SecurityEvent, ThreatHuntingResult
from ..core.config import settings
from .ml.anomaly_detection import AnomalyDetector
from .threat_intelligence import ThreatIntelligence
import logging

logger = logging.getLogger(__name__)

class ThreatHuntingService:
    def __init__(self):
        self.anomaly_detector = AnomalyDetector()
        self.threat_intel = ThreatIntelligence()
        self.hunting_patterns = {
            "lateral_movement": self._detect_lateral_movement,
            "privilege_escalation": self._detect_privilege_escalation,
            "data_staging": self._detect_data_staging,
            "c2_communication": self._detect_c2_communication,
            "persistence_mechanisms": self._detect_persistence
        }

    async def hunt_threats(self, timeframe: timedelta = timedelta(hours=24)) -> List[ThreatHuntingResult]:
        """Proactively hunt for threats"""
        try:
            # Get historical data for analysis
            start_time = datetime.utcnow() - timeframe
            events = await self._get_historical_events(start_time)

            # Run all hunting patterns in parallel
            hunting_tasks = [
                pattern_func(events)
                for pattern_func in self.hunting_patterns.values()
            ]
            
            results = await asyncio.gather(*hunting_tasks)
            return [result for result in results if result.threats_found]

        except Exception as e:
            logger.error(f"Error in threat hunting: {str(e)}")
            raise

    async def _detect_lateral_movement(self, events: List[SecurityEvent]) -> ThreatHuntingResult:
        """Detect lateral movement patterns"""
        try:
            # Group events by source IP
            ip_connections = self._group_by_source_ip(events)
            
            suspicious_ips = []
            for ip, connections in ip_connections.items():
                # Check for multiple internal connections
                if self._is_suspicious_lateral_movement(connections):
                    suspicious_ips.append(ip)

            return ThreatHuntingResult(
                pattern_type="lateral_movement",
                threats_found=len(suspicious_ips) > 0,
                indicators=suspicious_ips,
                confidence=self._calculate_confidence(suspicious_ips)
            )

        except Exception as e:
            logger.error(f"Error detecting lateral movement: {str(e)}")
            raise

    async def _detect_privilege_escalation(self, events: List[SecurityEvent]) -> ThreatHuntingResult:
        """Detect privilege escalation attempts"""
        try:
            suspicious_events = []
            for event in events:
                if self._is_privilege_escalation_attempt(event):
                    suspicious_events.append(event)

            return ThreatHuntingResult(
                pattern_type="privilege_escalation",
                threats_found=len(suspicious_events) > 0,
                indicators=[event.id for event in suspicious_events],
                confidence=self._calculate_confidence(suspicious_events)
            )

        except Exception as e:
            logger.error(f"Error detecting privilege escalation: {str(e)}")
            raise

    async def _detect_c2_communication(self, events: List[SecurityEvent]) -> ThreatHuntingResult:
        """Detect command and control communication patterns"""
        try:
            # Get known C2 indicators from threat intelligence
            c2_indicators = await self.threat_intel.get_c2_indicators()
            
            suspicious_comms = []
            for event in events:
                if self._matches_c2_pattern(event, c2_indicators):
                    suspicious_comms.append(event)

            return ThreatHuntingResult(
                pattern_type="c2_communication",
                threats_found=len(suspicious_comms) > 0,
                indicators=[{
                    "event_id": event.id,
                    "destination": event.destination_ip,
                    "pattern": event.pattern_matched
                } for event in suspicious_comms],
                confidence=self._calculate_confidence(suspicious_comms)
            )

        except Exception as e:
            logger.error(f"Error detecting C2 communication: {str(e)}")
            raise

    def _is_suspicious_lateral_movement(self, connections: List[Dict]) -> bool:
        """Analyze connections for suspicious lateral movement"""
        # Check for:
        # 1. Multiple connections to different internal hosts
        # 2. Unusual port sequences
        # 3. Time-based patterns
        unique_destinations = len(set(conn['destination'] for conn in connections))
        unique_ports = len(set(conn['port'] for conn in connections))
        
        return (
            unique_destinations > settings.LATERAL_MOVEMENT_HOST_THRESHOLD and
            unique_ports > settings.LATERAL_MOVEMENT_PORT_THRESHOLD
        )

    def _matches_c2_pattern(self, event: SecurityEvent, indicators: List[Dict]) -> bool:
        """Check if event matches known C2 patterns"""
        # Check for:
        # 1. Known C2 infrastructure
        # 2. Beaconing patterns
        # 3. Unusual protocols or ports
        # 4. Domain generation algorithms
        return any(
            self._matches_indicator(event, indicator)
            for indicator in indicators
        )

    def _calculate_confidence(self, indicators: List[Any]) -> float:
        """Calculate confidence score for detected threats"""
        if not indicators:
            return 0.0
            
        # Implement confidence scoring based on:
        # - Number of indicators
        # - Quality of matches
        # - Historical accuracy
        base_score = min(len(indicators) * 0.1, 0.6)
        quality_score = self._assess_indicator_quality(indicators)
        
        return min(base_score + quality_score, 1.0) 