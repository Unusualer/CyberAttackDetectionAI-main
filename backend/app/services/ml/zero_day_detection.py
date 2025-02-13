from typing import Dict, Any, List, Optional
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPRegressor
from .base import BaseMLModel
from ...core.config import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ZeroDayDetector(BaseMLModel):
    def __init__(self):
        super().__init__(f"{settings.MODEL_PATH}/zero_day_detector")
        self.isolation_forest = None
        self.autoencoder = None
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)  # Preserve 95% of variance
        self.threshold = settings.ZERO_DAY_THRESHOLD
        self.initialize_models()
        
    def initialize_models(self):
        """Initialize all detection models"""
        try:
            # Initialize Isolation Forest for outlier detection
            self.isolation_forest = IsolationForest(
                n_estimators=100,  # Reduced from 200 for CPU efficiency
                contamination=0.01,
                max_samples='auto',
                n_jobs=-1,  # Use all CPU cores
                random_state=42
            )
            
            # Initialize MLP-based autoencoder for CPU efficiency
            self.autoencoder = self._create_autoencoder()
            
        except Exception as e:
            logger.error(f"Error initializing zero-day detector: {str(e)}")
            raise
            
    def _create_autoencoder(self) -> MLPRegressor:
        """Create MLP-based autoencoder for CPU-efficient processing"""
        return MLPRegressor(
            hidden_layer_sizes=(64, 32, 64),  # Smaller network for CPU
            activation='relu',
            solver='adam',
            max_iter=200,
            early_stopping=True,
            n_iter_no_change=10,
            verbose=False
        )
        
    async def detect_zero_day(self, features: np.ndarray) -> Dict[str, Any]:
        """Detect potential zero-day attacks using multiple methods"""
        try:
            # Normalize features
            scaled_features = self.scaler.transform(features)
            
            # 1. Isolation Forest Detection (efficient on CPU)
            if_scores = self.isolation_forest.score_samples(scaled_features)
            if_probs = np.exp(if_scores) / (1 + np.exp(if_scores))
            
            # 2. Autoencoder Reconstruction
            reconstructed = self.autoencoder.predict(scaled_features)
            reconstruction_errors = np.mean(np.square(scaled_features - reconstructed.reshape(scaled_features.shape)), axis=1)
            
            # 3. PCA Transformation and Analysis
            pca_features = self.pca.transform(scaled_features)
            pca_reconstructed = self.pca.inverse_transform(pca_features)
            pca_errors = np.mean(np.square(scaled_features - pca_reconstructed), axis=1)
            
            # Combine detection methods
            combined_score = self._combine_detection_scores(
                if_probs,
                reconstruction_errors,
                pca_errors
            )
            
            # Determine if it's a potential zero-day attack
            is_zero_day = combined_score < self.threshold
            
            return {
                "is_zero_day": bool(is_zero_day),
                "confidence": float(abs(combined_score - self.threshold)),
                "anomaly_scores": {
                    "isolation_forest": float(if_probs[0]),
                    "autoencoder": float(reconstruction_errors[0]),
                    "pca": float(pca_errors[0])
                },
                "details": self._generate_detection_details(
                    scaled_features,
                    reconstructed.reshape(scaled_features.shape),
                    pca_reconstructed
                )
            }
            
        except Exception as e:
            logger.error(f"Error in zero-day detection: {str(e)}")
            raise
            
    def _combine_detection_scores(
        self,
        if_scores: np.ndarray,
        ae_errors: np.ndarray,
        pca_errors: np.ndarray
    ) -> float:
        """Combine scores from different detection methods"""
        # Normalize errors to [0, 1] range
        ae_scores = 1 - (ae_errors / (np.max(ae_errors) + 1e-10))
        pca_scores = 1 - (pca_errors / (np.max(pca_errors) + 1e-10))
        
        # Weighted combination
        weights = [0.4, 0.4, 0.2]  # Isolation Forest, Autoencoder, PCA
        combined = (
            weights[0] * if_scores +
            weights[1] * ae_scores +
            weights[2] * pca_scores
        )
        
        return float(np.mean(combined))
        
    def _generate_detection_details(
        self,
        original: np.ndarray,
        ae_reconstructed: np.ndarray,
        pca_reconstructed: np.ndarray
    ) -> Dict[str, Any]:
        """Generate detailed analysis of the detection"""
        return {
            "feature_importance": self._calculate_feature_importance(
                original,
                ae_reconstructed
            ),
            "reconstruction_analysis": {
                "autoencoder_diff": float(np.mean(np.abs(original - ae_reconstructed))),
                "pca_diff": float(np.mean(np.abs(original - pca_reconstructed)))
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    def _calculate_feature_importance(
        self,
        original: np.ndarray,
        reconstructed: np.ndarray
    ) -> Dict[str, float]:
        """Calculate feature importance based on reconstruction error"""
        feature_errors = np.mean(np.square(original - reconstructed), axis=0)
        total_error = np.sum(feature_errors) + 1e-10  # Avoid division by zero
        
        return {
            f"feature_{i}": float(error / total_error)
            for i, error in enumerate(feature_errors)
        }
        
    async def train(
        self,
        X_train: np.ndarray,
        validation_data: Optional[tuple] = None,
        epochs: int = 10
    ):
        """Train the zero-day detection models"""
        try:
            # Fit the scaler
            self.scaler.fit(X_train)
            X_scaled = self.scaler.transform(X_train)
            
            # Fit PCA
            self.pca.fit(X_scaled)
            
            # Train Isolation Forest (parallel processing)
            self.isolation_forest.fit(X_scaled)
            
            # Train Autoencoder
            self.autoencoder.fit(X_scaled, X_scaled)  # Autoencoder reconstructs input
            
            return {
                "isolation_forest_score": self.isolation_forest.score_samples(X_scaled).mean(),
                "autoencoder_loss": self.autoencoder.loss_,
                "n_iter": self.autoencoder.n_iter_
            }
            
        except Exception as e:
            logger.error(f"Error training zero-day detector: {str(e)}")
            raise
            
    def save(self):
        """Save all models and preprocessors"""
        try:
            import joblib
            
            # Save all components
            joblib.dump(self.isolation_forest, f"{self.model_path}_isolation_forest.pkl")
            joblib.dump(self.autoencoder, f"{self.model_path}_autoencoder.pkl")
            joblib.dump(self.scaler, f"{self.model_path}_scaler.pkl")
            joblib.dump(self.pca, f"{self.model_path}_pca.pkl")
            
        except Exception as e:
            logger.error(f"Error saving zero-day detector: {str(e)}")
            raise
            
    def load_model(self):
        """Load all models and preprocessors"""
        try:
            import joblib
            
            # Load all components
            self.isolation_forest = joblib.load(f"{self.model_path}_isolation_forest.pkl")
            self.autoencoder = joblib.load(f"{self.model_path}_autoencoder.pkl")
            self.scaler = joblib.load(f"{self.model_path}_scaler.pkl")
            self.pca = joblib.load(f"{self.model_path}_pca.pkl")
            
        except Exception as e:
            logger.error(f"Error loading zero-day detector: {str(e)}")
            # Initialize new models if loading fails
            self.initialize_models() 