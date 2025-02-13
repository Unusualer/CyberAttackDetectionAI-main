from abc import ABC, abstractmethod
import numpy as np
from typing import List, Dict, Any
from ...schemas.schemas import SecurityEvent
import tensorflow as tf
import joblib
from ...core.config import settings

class BaseMLModel(ABC):
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = self.load_model()
        
    @abstractmethod
    def load_model(self):
        """Load the ML model"""
        pass
        
    @abstractmethod
    def predict(self, features: np.ndarray) -> np.ndarray:
        """Make predictions using the model"""
        pass
        
    @abstractmethod
    def train(self, X: np.ndarray, y: np.ndarray):
        """Train/retrain the model"""
        pass
        
    @abstractmethod
    def save(self):
        """Save the model"""
        pass

class MLModelManager:
    def __init__(self):
        self.anomaly_detector = None
        self.threat_classifier = None
        self.behavior_analyzer = None
        self.initialize_models()
        
    def initialize_models(self):
        """Initialize all ML models"""
        try:
            self.anomaly_detector = self.load_model("anomaly_detector")
            self.threat_classifier = self.load_model("threat_classifier")
            self.behavior_analyzer = self.load_model("behavior_analyzer")
        except Exception as e:
            logger.error(f"Error initializing ML models: {str(e)}")
            raise
            
    def load_model(self, model_name: str):
        """Load a specific model"""
        model_path = f"{settings.MODEL_PATH}/{model_name}"
        if model_name.endswith("_tf"):
            return tf.keras.models.load_model(model_path)
        return joblib.load(model_path) 