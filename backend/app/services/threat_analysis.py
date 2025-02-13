from typing import Dict, Any, List
import numpy as np
from .ml.anomaly_detection import AnomalyDetector
from .ml.threat_classifier import ThreatClassifier
from ..schemas.schemas import SecurityEvent
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class ThreatAnalysisService:
    def __init__(self):
        self.anomaly_detector = AnomalyDetector()
        self.threat_classifier = ThreatClassifier()
        
    async def analyze_event(self, event: SecurityEvent) -> Dict[str, Any]:
        """Analyze a security event for threats"""
        try:
            # Extract features
            features = self._extract_features(event)
            
            # Detect anomalies
            anomaly_result = self.anomaly_detector.predict(features)
            
            # If anomaly detected, classify the threat
            threat_result = None
            if anomaly_result["is_anomaly"]:
                threat_result = self.threat_classifier.predict(features)
                
            return {
                "event_id": event.id,
                "anomaly_detection": anomaly_result,
                "threat_classification": threat_result,
                "risk_score": self._calculate_risk_score(
                    anomaly_result,
                    threat_result
                )
            }
            
        except Exception as e:
            logger.error(f"Error in threat analysis: {str(e)}")
            raise
            
    def _extract_features(self, event: SecurityEvent) -> np.ndarray:
        """Extract features from security event"""
        # Implement feature extraction based on your event data
        # This is a placeholder
        features = np.zeros(50)  # Adjust size based on your model
        return features.reshape(1, -1)
        
    def _calculate_risk_score(
        self,
        anomaly_result: Dict[str, Any],
        threat_result: Dict[str, Any]
    ) -> float:
        """Calculate overall risk score"""
        base_score = anomaly_result["anomaly_score"] * 100
        
        if threat_result:
            # Adjust score based on threat type
            threat_multipliers = {
                "malware": 1.5,
                "phishing": 1.3,
                "ddos": 1.4,
                "intrusion": 1.6,
                "data_exfiltration": 1.8
            }
            
            multiplier = threat_multipliers.get(
                threat_result["threat_type"],
                1.0
            )
            base_score *= multiplier
            
        return min(100, base_score) 