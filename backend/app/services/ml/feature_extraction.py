from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from sklearn.feature_selection import VarianceThreshold, mutual_info_classif
from sklearn.preprocessing import StandardScaler, RobustScaler
from ...core.config import settings
import logging
from datetime import datetime
import psutil
from numba import jit
import pandas as pd
from dask import dataframe as dd

logger = logging.getLogger(__name__)

class FeatureExtractor:
    def __init__(self):
        self.scaler = RobustScaler()  # More robust to outliers
        self.feature_selector = None
        self.selected_features: List[int] = []
        self.feature_names: List[str] = []
        self._initialize_metrics()
        
    def _initialize_metrics(self):
        """Initialize performance metrics tracking"""
        self.metrics = {
            "processed_events": 0,
            "processing_time": 0.0,
            "memory_usage": 0.0,
            "last_update": datetime.now()
        }
        
    @jit(nopython=True)
    def _normalize_numeric(self, value: float) -> float:
        """Normalize numeric values with JIT compilation"""
        if np.isnan(value) or np.isinf(value):
            return 0.0
        return float(value)
        
    def extract_network_features(self, event_data: Dict[str, Any]) -> np.ndarray:
        """Extract network-related features with enhanced error handling"""
        try:
            features = []
            for feature in settings.NETWORK_FEATURES:
                value = event_data.get(feature, 0)
                if isinstance(value, str):
                    # Enhanced categorical encoding
                    try:
                        value = self._encode_categorical(value, feature)
                    except Exception as e:
                        logger.warning(f"Error encoding {feature}: {str(e)}")
                        value = 0
                features.append(self._normalize_numeric(float(value)))
            return np.array(features)
        except Exception as e:
            logger.error(f"Error extracting network features: {str(e)}")
            return np.zeros(len(settings.NETWORK_FEATURES))
            
    def _encode_categorical(self, value: str, feature_name: str) -> float:
        """Enhanced categorical encoding with feature-specific handling"""
        if feature_name == "protocol":
            protocols = {"tcp": 1, "udp": 2, "icmp": 3}
            return float(protocols.get(value.lower(), 0))
        elif feature_name == "flags":
            return float(len(value))  # Count flags as a feature
        else:
            return float(hash(value) % 100)  # Fallback to hash encoding
            
    def extract_system_features(self, event_data: Dict[str, Any]) -> np.ndarray:
        """Extract system-related features with validation"""
        try:
            features = []
            for feature in settings.SYSTEM_FEATURES:
                value = event_data.get(feature, 0)
                # Validate and normalize system metrics
                if feature in ["cpu_usage", "memory_usage"]:
                    value = min(max(float(value), 0), 100)  # Ensure 0-100 range
                elif feature == "process_count":
                    value = max(float(value), 0)  # Ensure non-negative
                features.append(self._normalize_numeric(float(value)))
            return np.array(features)
        except Exception as e:
            logger.error(f"Error extracting system features: {str(e)}")
            return np.zeros(len(settings.SYSTEM_FEATURES))
            
    def extract_user_features(self, event_data: Dict[str, Any]) -> np.ndarray:
        """Extract user behavior features with anomaly checks"""
        try:
            features = []
            for feature in settings.USER_FEATURES:
                value = event_data.get(feature, 0)
                # Check for anomalous values
                if isinstance(value, (int, float)):
                    if value < 0 or value > settings.MAX_USER_FEATURE_VALUE:
                        logger.warning(f"Anomalous value for {feature}: {value}")
                        value = min(max(float(value), 0), settings.MAX_USER_FEATURE_VALUE)
                features.append(self._normalize_numeric(float(value)))
            return np.array(features)
        except Exception as e:
            logger.error(f"Error extracting user features: {str(e)}")
            return np.zeros(len(settings.USER_FEATURES))
            
    def combine_features(
        self,
        network_features: np.ndarray,
        system_features: np.ndarray,
        user_features: np.ndarray
    ) -> np.ndarray:
        """Combine features with importance weighting"""
        try:
            # Apply feature importance weights
            weighted_features = np.concatenate([
                network_features * settings.NETWORK_FEATURE_WEIGHT,
                system_features * settings.SYSTEM_FEATURE_WEIGHT,
                user_features * settings.USER_FEATURE_WEIGHT
            ])
            return weighted_features
        except Exception as e:
            logger.error(f"Error combining features: {str(e)}")
            total_features = (
                len(settings.NETWORK_FEATURES) +
                len(settings.SYSTEM_FEATURES) +
                len(settings.USER_FEATURES)
            )
            return np.zeros(total_features)
            
    def select_features(
        self,
        X: np.ndarray,
        y: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, List[str]]:
        """Select features with importance ranking"""
        if not settings.ENABLE_FEATURE_SELECTION:
            return X, self.get_feature_names()
            
        try:
            if settings.FEATURE_SELECTION_METHOD == "variance":
                if self.feature_selector is None:
                    self.feature_selector = VarianceThreshold(threshold=0.01)
                    self.feature_selector.fit(X)
                    self.selected_features = self.feature_selector.get_support(indices=True)
                
                selected_X = self.feature_selector.transform(X)
                selected_names = [self.feature_names[i] for i in self.selected_features]
                return selected_X, selected_names
                
            elif settings.FEATURE_SELECTION_METHOD == "mutual_info" and y is not None:
                if self.feature_selector is None:
                    mi_scores = mutual_info_classif(X, y)
                    # Select top features with importance scores
                    self.selected_features = np.argsort(mi_scores)[-settings.MAX_FEATURES:]
                    # Store importance scores
                    self.feature_importance = {
                        self.feature_names[i]: float(mi_scores[i])
                        for i in self.selected_features
                    }
                
                selected_X = X[:, self.selected_features]
                selected_names = [self.feature_names[i] for i in self.selected_features]
                return selected_X, selected_names
                
            return X, self.get_feature_names()
            
        except Exception as e:
            logger.error(f"Error in feature selection: {str(e)}")
            return X, self.get_feature_names()
            
    def process_batch(
        self,
        events: List[Dict[str, Any]],
        batch_size: Optional[int] = None
    ) -> np.ndarray:
        """Process events with memory optimization and progress tracking"""
        start_time = datetime.now()
        
        try:
            if not batch_size:
                # Dynamically adjust batch size based on available memory
                available_memory = psutil.virtual_memory().available
                batch_size = min(
                    settings.MAX_BATCH_SIZE,
                    max(settings.MIN_BATCH_SIZE, int(available_memory / (1024 * 1024 * 10)))
                )
                
            # Convert to Dask DataFrame for out-of-core processing
            df = pd.DataFrame(events)
            ddf = dd.from_pandas(df, npartitions=max(1, len(events) // batch_size))
            
            # Process in parallel with progress tracking
            processed_features = []
            total_batches = int(np.ceil(len(events) / batch_size))
            
            for i, batch_df in enumerate(ddf.partitions):
                batch = batch_df.compute().to_dict('records')
                batch_features = []
                
                for event in batch:
                    network_features = self.extract_network_features(event)
                    system_features = self.extract_system_features(event)
                    user_features = self.extract_user_features(event)
                    
                    combined = self.combine_features(
                        network_features,
                        system_features,
                        user_features
                    )
                    batch_features.append(combined)
                    
                batch_features = np.array(batch_features)
                
                # Incremental scaling for memory efficiency
                if not self.scaler.n_samples_seen_:
                    batch_features = self.scaler.fit_transform(batch_features)
                else:
                    batch_features = self.scaler.transform(batch_features)
                    
                processed_features.append(batch_features)
                
                # Update metrics
                self._update_metrics(len(batch), start_time)
                
                # Log progress
                if (i + 1) % max(1, total_batches // 10) == 0:
                    logger.info(f"Processed {i + 1}/{total_batches} batches")
                    
            return np.vstack(processed_features)
            
        except Exception as e:
            logger.error(f"Error in batch processing: {str(e)}")
            raise
            
    def _update_metrics(self, batch_size: int, start_time: datetime):
        """Update performance metrics"""
        self.metrics["processed_events"] += batch_size
        self.metrics["processing_time"] = (datetime.now() - start_time).total_seconds()
        self.metrics["memory_usage"] = psutil.Process().memory_info().rss / (1024 * 1024)
        self.metrics["last_update"] = datetime.now()
        
    def get_feature_names(self) -> List[str]:
        """Get feature names with descriptions"""
        if not self.feature_names:
            self.feature_names = (
                [f"network_{f}" for f in settings.NETWORK_FEATURES] +
                [f"system_{f}" for f in settings.SYSTEM_FEATURES] +
                [f"user_{f}" for f in settings.USER_FEATURES]
            )
        return self.feature_names
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            **self.metrics,
            "features_selected": len(self.selected_features),
            "total_features": len(self.get_feature_names()),
            "feature_importance": getattr(self, 'feature_importance', {})
        }
        
    def save(self, path: str):
        """Save feature extraction state with versioning"""
        try:
            import joblib
            state = {
                "scaler": self.scaler,
                "feature_selector": self.feature_selector,
                "selected_features": self.selected_features,
                "feature_names": self.feature_names,
                "metrics": self.metrics,
                "feature_importance": getattr(self, 'feature_importance', {}),
                "version": "2.0.0",  # Add versioning
                "timestamp": datetime.now().isoformat()
            }
            joblib.dump(state, path)
            logger.info(f"Feature extraction state saved to {path}")
        except Exception as e:
            logger.error(f"Error saving feature extraction state: {str(e)}")
            raise
            
    def load(self, path: str):
        """Load feature extraction state with version checking"""
        try:
            import joblib
            state = joblib.load(path)
            
            # Version compatibility check
            if state.get("version", "1.0.0") >= "2.0.0":
                self.scaler = state["scaler"]
                self.feature_selector = state["feature_selector"]
                self.selected_features = state["selected_features"]
                self.feature_names = state["feature_names"]
                self.metrics = state["metrics"]
                if "feature_importance" in state:
                    self.feature_importance = state["feature_importance"]
                    
                logger.info(f"Feature extraction state loaded from {path}")
            else:
                logger.warning("Outdated feature extraction state version")
                self._initialize_metrics()
                
        except Exception as e:
            logger.error(f"Error loading feature extraction state: {str(e)}")
            self._initialize_metrics() 