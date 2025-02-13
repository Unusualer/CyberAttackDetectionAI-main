from typing import Dict, Any, List
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import tensorflow as tf
import logging

logger = logging.getLogger(__name__)

class ModelEvaluator:
    def __init__(self):
        self.metrics = ["accuracy", "precision", "recall", "f1"]
        self.thresholds = {
            "accuracy": 0.9,
            "precision": 0.85,
            "recall": 0.85,
            "f1": 0.87
        }
        
    async def evaluate_model(
        self,
        model: Any,
        test_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """Evaluate model performance"""
        try:
            # Get predictions
            predictions = await self._get_predictions(model, test_data["X_test"])
            
            # Calculate metrics
            metrics = {}
            y_true = test_data["y_test"]
            
            metrics["accuracy"] = accuracy_score(y_true, predictions)
            metrics["precision"] = precision_score(y_true, predictions, average='weighted')
            metrics["recall"] = recall_score(y_true, predictions, average='weighted')
            metrics["f1"] = f1_score(y_true, predictions, average='weighted')
            
            # Add additional metrics
            metrics["confusion_matrix"] = self._calculate_confusion_matrix(
                y_true,
                predictions
            )
            metrics["roc_auc"] = self._calculate_roc_auc(
                y_true,
                predictions
            )
            
            # Validate metrics
            self._validate_metrics(metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error evaluating model: {str(e)}")
            raise
            
    async def _get_predictions(self, model: Any, X_test: np.ndarray) -> np.ndarray:
        """Get model predictions"""
        if isinstance(model, tf.keras.Model):
            predictions = model.predict(X_test)
            return np.argmax(predictions, axis=1)
        return model.predict(X_test)
        
    def _validate_metrics(self, metrics: Dict[str, float]):
        """Validate metrics against thresholds"""
        for metric, value in metrics.items():
            if metric in self.thresholds:
                if value < self.thresholds[metric]:
                    logger.warning(
                        f"{metric} below threshold: {value:.3f} < {self.thresholds[metric]}"
                    )
                    
    def _calculate_confusion_matrix(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> List[List[int]]:
        """Calculate confusion matrix"""
        from sklearn.metrics import confusion_matrix
        return confusion_matrix(y_true, y_pred).tolist()
        
    def _calculate_roc_auc(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> float:
        """Calculate ROC AUC score"""
        from sklearn.metrics import roc_auc_score
        try:
            return roc_auc_score(y_true, y_pred, multi_class='ovr')
        except:
            return 0.0