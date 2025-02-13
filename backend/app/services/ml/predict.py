import numpy as np
from typing import Dict, List, Optional, Tuple
from data_manager import DataManager
from training_pipeline import ModelTrainingPipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatPredictor:
    def __init__(self):
        """Initialize the threat predictor with trained models."""
        self.data_manager = DataManager()
        self.pipeline = ModelTrainingPipeline(self.data_manager)
        self.pipeline.load_models()
        
    def predict_threats(self, events: List[Dict]) -> List[Dict]:
        """
        Predict threats from network events.
        
        Args:
            events: List of dictionaries containing network event data
                   Each event should have the following fields:
                   - bytes_sent: int
                   - bytes_received: int
                   - packets_sent: int
                   - packets_received: int
                   - duration: float
                   
        Returns:
            List of dictionaries containing predictions for each event
        """
        try:
            # Convert events to DataFrame
            import pandas as pd
            df = pd.DataFrame(events)
            
            # Preprocess data
            X, _ = self.data_manager.preprocess_data(df)
            
            # Make predictions
            anomaly_preds, threat_preds = self.pipeline.predict(X)
            
            # Prepare results
            results = []
            for i, event in enumerate(events):
                result = {
                    "event": event,
                    "predictions": {
                        "is_anomaly": bool(anomaly_preds[i]) if anomaly_preds is not None else None,
                        "is_threat": bool(threat_preds[i]) if threat_preds is not None else None
                    },
                    "timestamp": pd.Timestamp.now().isoformat()
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error making predictions: {str(e)}")
            raise
    
    def get_threat_details(self, predictions: List[Dict]) -> Dict:
        """
        Get detailed information about detected threats.
        
        Args:
            predictions: List of prediction results from predict_threats()
            
        Returns:
            Dictionary containing threat statistics and details
        """
        try:
            # Count threats and anomalies
            n_anomalies = sum(1 for p in predictions if p["predictions"]["is_anomaly"])
            n_threats = sum(1 for p in predictions if p["predictions"]["is_threat"])
            
            # Get attack patterns for context
            attack_patterns = self.data_manager.get_attack_patterns()
            
            # Prepare threat report
            report = {
                "summary": {
                    "total_events": len(predictions),
                    "anomalies_detected": n_anomalies,
                    "threats_detected": n_threats,
                    "timestamp": pd.Timestamp.now().isoformat()
                },
                "threat_events": [
                    p for p in predictions 
                    if p["predictions"]["is_threat"] or p["predictions"]["is_anomaly"]
                ],
                "attack_patterns": attack_patterns
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating threat details: {str(e)}")
            raise

def main():
    """Example usage of ThreatPredictor."""
    try:
        # Initialize predictor
        predictor = ThreatPredictor()
        
        # Generate some sample events
        sample_events = [
            {
                "bytes_sent": 1000,
                "bytes_received": 2000,
                "packets_sent": 10,
                "packets_received": 20,
                "duration": 30.0
            },
            {
                "bytes_sent": 100000,  # Unusual amount of data
                "bytes_received": 500,
                "packets_sent": 1000,
                "packets_received": 5,
                "duration": 1.0  # Very short duration
            }
        ]
        
        # Make predictions
        logger.info("Making predictions on sample events...")
        predictions = predictor.predict_threats(sample_events)
        
        # Get threat details
        logger.info("Generating threat report...")
        threat_report = predictor.get_threat_details(predictions)
        
        # Print results
        logger.info("\nPrediction Results:")
        for pred in predictions:
            logger.info(f"Event: {pred['event']}")
            logger.info(f"Predictions: {pred['predictions']}\n")
            
        logger.info("\nThreat Report:")
        logger.info(f"Total Events: {threat_report['summary']['total_events']}")
        logger.info(f"Anomalies Detected: {threat_report['summary']['anomalies_detected']}")
        logger.info(f"Threats Detected: {threat_report['summary']['threats_detected']}")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 