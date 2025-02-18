from typing import Dict, Tuple
import logging
from .keras_model import NetworkIntrusionDetector
import joblib
import os
import numpy as np

logger = logging.getLogger(__name__)

class ThreatDetector:
    def __init__(self):
        self.keras_detector = NetworkIntrusionDetector()
        self.isolation_forest = None
        self.model_path = os.getenv("MODEL_PATH", "/app/ai/models")
        
    def load_models(self):
        """Load both models if not already loaded"""
        if self.isolation_forest is None:
            iso_forest_path = os.path.join(self.model_path, "isolation_forest.joblib")
            self.isolation_forest = joblib.load(iso_forest_path)
        
        # Keras model is loaded on-demand in its class
        
    def detect_threats(self, event_data: Dict) -> Dict:
        """
        Analyze event using both models for more robust detection
        """
        try:
            self.load_models()
            
            # Get Keras model prediction
            attack_type, confidence = self.keras_detector.predict(event_data)
            
            # Get Isolation Forest anomaly score
            features = self.keras_detector.preprocess_data(event_data)
            iso_forest_score = self.isolation_forest.score_samples(features)[0]
            
            # Combine results
            is_anomaly = iso_forest_score < -0.5  # Threshold for isolation forest
            
            return {
                "is_threat": is_anomaly or attack_type != "normal",
                "attack_type": attack_type,
                "confidence": confidence,
                "anomaly_score": float(iso_forest_score),
                "severity": self._calculate_severity(confidence, iso_forest_score)
            }
            
        except Exception as e:
            logger.error(f"Error in threat detection: {str(e)}")
            raise
            
    def _calculate_severity(self, confidence: float, anomaly_score: float) -> str:
        """Calculate severity based on both models' scores"""
        if confidence > 0.9 or anomaly_score < -0.8:
            return "critical"
        elif confidence > 0.7 or anomaly_score < -0.6:
            return "high"
        elif confidence > 0.5 or anomaly_score < -0.4:
            return "medium"
        else:
            return "low" 