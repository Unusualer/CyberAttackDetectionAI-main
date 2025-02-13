from typing import Dict, Any
import numpy as np
from ..schemas.schemas import ThreatScore, SecurityEvent
from ..core.config import settings

class ThreatScoringEngine:
    def __init__(self):
        self.weights = {
            "severity": 0.3,
            "confidence": 0.2,
            "impact": 0.25,
            "complexity": 0.15,
            "context": 0.1
        }
        
    async def calculate_threat_score(self, event: SecurityEvent) -> ThreatScore:
        """Calculate comprehensive threat score"""
        base_score = self._calculate_base_score(event)
        temporal_score = self._calculate_temporal_score(event)
        environmental_score = self._calculate_environmental_score(event)
        
        final_score = (
            base_score * 0.6 +
            temporal_score * 0.25 +
            environmental_score * 0.15
        )
        
        return ThreatScore(
            score=final_score,
            base_score=base_score,
            temporal_score=temporal_score,
            environmental_score=environmental_score,
            factors=self._get_contributing_factors(event)
        ) 
        
    def _calculate_base_score(self, event: SecurityEvent) -> float:
        """Calculate base threat score"""
        severity_score = self._normalize_severity(event.severity)
        impact_score = self._calculate_impact_score(event)
        complexity_score = self._calculate_complexity_score(event)
        
        return (
            severity_score * self.weights["severity"] +
            impact_score * self.weights["impact"] +
            complexity_score * self.weights["complexity"]
        )
        
    def _calculate_temporal_score(self, event: SecurityEvent) -> float:
        """Calculate temporal score based on time-based factors"""
        # Consider factors like:
        # - Time of day
        # - Day of week
        # - Recent similar events
        # - Current threat landscape
        
        time_factor = self._calculate_time_factor(event.timestamp)
        frequency_factor = self._calculate_frequency_factor(event)
        
        return (time_factor + frequency_factor) / 2
        
    def _calculate_environmental_score(self, event: SecurityEvent) -> float:
        """Calculate environmental score based on context"""
        # Consider factors like:
        # - Asset criticality
        # - Network segment
        # - Current system state
        # - User context
        
        asset_criticality = self._get_asset_criticality(event.target)
        network_exposure = self._calculate_network_exposure(event)
        system_state = self._get_system_state(event.timestamp)
        
        return (
            asset_criticality * 0.4 +
            network_exposure * 0.3 +
            system_state * 0.3
        )
        
    def _get_contributing_factors(self, event: SecurityEvent) -> Dict[str, Any]:
        """Get detailed breakdown of factors contributing to score"""
        return {
            "severity": {
                "score": self._normalize_severity(event.severity),
                "weight": self.weights["severity"],
                "factors": self._get_severity_factors(event)
            },
            "impact": {
                "score": self._calculate_impact_score(event),
                "weight": self.weights["impact"],
                "factors": self._get_impact_factors(event)
            },
            "temporal": {
                "time_factor": self._calculate_time_factor(event.timestamp),
                "frequency_factor": self._calculate_frequency_factor(event)
            },
            "environmental": {
                "asset_criticality": self._get_asset_criticality(event.target),
                "network_exposure": self._calculate_network_exposure(event),
                "system_state": self._get_system_state(event.timestamp)
            }
        } 