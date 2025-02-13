import numpy as np
import tensorflow as tf
from .base import BaseMLModel
from ...core.config import settings
import logging

logger = logging.getLogger(__name__)

class ThreatClassifier(BaseMLModel):
    def __init__(self):
        super().__init__(f"{settings.MODEL_PATH}/threat_classifier")
        self.classes = [
            "normal",
            "malware",
            "phishing",
            "ddos",
            "intrusion",
            "data_exfiltration"
        ]
        
    def load_model(self):
        """Load the deep learning model"""
        try:
            return tf.keras.models.load_model(self.model_path)
        except Exception as e:
            logger.error(f"Error loading threat classifier: {str(e)}")
            # If model doesn't exist, create a new one
            return self._create_model()
            
    def _create_model(self):
        """Create a new model if none exists"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(50,)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(len(self.classes), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
        
    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """Classify the type of threat"""
        try:
            # Get prediction probabilities
            probs = self.model.predict(features)
            
            # Get the predicted class
            pred_class = self.classes[np.argmax(probs)]
            
            return {
                "threat_type": pred_class,
                "confidence": float(np.max(probs)),
                "probabilities": {
                    class_name: float(prob)
                    for class_name, prob in zip(self.classes, probs[0])
                }
            }
        except Exception as e:
            logger.error(f"Error in threat classification: {str(e)}")
            raise 