import numpy as np
from sklearn.ensemble import IsolationForest
from .base import BaseMLModel
from ...core.config import settings
import logging

logger = logging.getLogger(__name__)

class AnomalyDetector(BaseMLModel):
    def __init__(self):
        super().__init__(f"{settings.MODEL_PATH}/anomaly_detector")
        self.threshold = settings.ANOMALY_THRESHOLD
        
    def load_model(self):
        try:
            return IsolationForest(
                n_estimators=100,
                contamination=0.1,
                random_state=42
            )
        except Exception as e:
            logger.error(f"Error loading anomaly detector: {str(e)}")
            raise
            
    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """Detect anomalies in network traffic"""
        try:
            # Get anomaly scores
            scores = self.model.score_samples(features)
            
            # Convert to probability-like values
            probs = np.exp(scores) / (1 + np.exp(scores))
            
            # Detect anomalies
            is_anomaly = probs < self.threshold
            
            return {
                "is_anomaly": bool(is_anomaly),
                "anomaly_score": float(probs[0]),
                "confidence": float(abs(probs[0] - self.threshold))
            }
        except Exception as e:
            logger.error(f"Error in anomaly detection: {str(e)}")
            raise
            
    def train(self, X: np.ndarray, y: np.ndarray = None):
        """Train the anomaly detector"""
        try:
            self.model.fit(X)
            self.save()
        except Exception as e:
            logger.error(f"Error training anomaly detector: {str(e)}")
            raise 