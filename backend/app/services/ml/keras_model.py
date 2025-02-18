import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import joblib
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class NetworkIntrusionDetector:
    def __init__(self, model_path: str = None):
        self.model_path = model_path or os.getenv("MODEL_PATH", "/app/ai/models")
        self.model = None
        self.scaler = None
        self.feature_columns = [
            "bytes_sent", "bytes_received", 
            "packets_sent", "packets_received",
            "cpu_usage", "memory_usage", 
            "disk_io", "process_count",
            "login_attempts", "file_operations"
        ]
        
    def load_model(self) -> None:
        """Load the Keras model and scaler"""
        try:
            # Load the Keras model
            model_file = os.path.join(self.model_path, "network-intrusion-detection-model")
            self.model = keras.models.load_model(model_file)
            
            # Load the scaler
            scaler_file = os.path.join(self.model_path, "scaler.joblib")
            self.scaler = joblib.load(scaler_file)
            
            logger.info("Successfully loaded Keras model and scaler")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def preprocess_data(self, data: Dict) -> np.ndarray:
        """Preprocess input data for model prediction"""
        try:
            # Extract features in correct order
            features = np.array([[
                float(data.get(col, 0)) for col in self.feature_columns
            ]])
            
            # Scale features
            if self.scaler:
                features = self.scaler.transform(features)
                
            return features
        except Exception as e:
            logger.error(f"Error preprocessing data: {str(e)}")
            raise
    
    def predict(self, data: Dict) -> Tuple[str, float]:
        """Make prediction with confidence score"""
        try:
            if not self.model:
                self.load_model()
                
            # Preprocess the data
            features = self.preprocess_data(data)
            
            # Get model predictions
            predictions = self.model.predict(features)
            
            # Get the predicted class and confidence
            predicted_class = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class])
            
            # Map class index to attack type
            attack_types = {
                0: "normal",
                1: "dos_attack",
                2: "brute_force",
                3: "data_exfiltration"
            }
            
            return attack_types[predicted_class], confidence
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise 