from typing import List, Dict, Any
import numpy as np
from datetime import datetime, timedelta
from ..schemas.schemas import SecurityEvent, CorrelationResult
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class ThreatCorrelationService:
    def __init__(self):
        self.time_window = settings.CORRELATION_TIME_WINDOW
        self.correlation_threshold = settings.CORRELATION_THRESHOLD
        
    async def correlate_events(self, events: List[SecurityEvent]) -> List[CorrelationResult]:
        """Correlate multiple security events to identify attack patterns"""
        try:
            # Group events by time windows
            time_windows = self._group_by_time_window(events)
            
            # Analyze each time window
            correlations = []
            for window_events in time_windows:
                correlation = await self._analyze_window(window_events)
                if correlation.confidence > self.correlation_threshold:
                    correlations.append(correlation)
                    
            return correlations
            
        except Exception as e:
            logger.error(f"Error in threat correlation: {str(e)}")
            raise
            
    def _group_by_time_window(self, events: List[SecurityEvent]) -> List[List[SecurityEvent]]:
        """Group events into time windows for analysis"""
        # Implementation 
        
    async def _analyze_window(self, events: List[SecurityEvent]) -> CorrelationResult:
        """Analyze events within a time window for correlations"""
        try:
            # Extract features from events
            event_features = self._extract_event_features(events)
            
            # Find event clusters
            clusters = self._cluster_events(event_features)
            
            # Identify attack patterns
            patterns = self._identify_patterns(clusters)
            
            # Calculate correlation confidence
            confidence = self._calculate_correlation_confidence(patterns)
            
            return CorrelationResult(
                events=events,
                patterns=patterns,
                confidence=confidence,
                timestamp=datetime.utcnow(),
                details=self._generate_correlation_details(patterns)
            )
            
        except Exception as e:
            logger.error(f"Error analyzing event window: {str(e)}")
            raise
            
    def _extract_event_features(self, events: List[SecurityEvent]) -> np.ndarray:
        """Extract numerical features from events for analysis"""
        features = []
        for event in events:
            feature_vector = [
                event.severity,
                event.confidence,
                self._encode_event_type(event.type),
                self._calculate_impact_score(event),
                self._encode_source(event.source)
            ]
            features.append(feature_vector)
        return np.array(features)
        
    def _cluster_events(self, features: np.ndarray) -> List[Dict[str, Any]]:
        """Cluster similar events together"""
        from sklearn.cluster import DBSCAN
        
        # Use DBSCAN for clustering
        clustering = DBSCAN(
            eps=settings.CLUSTERING_DISTANCE,
            min_samples=settings.MIN_CLUSTER_SIZE
        ).fit(features)
        
        # Group events by cluster
        clusters = {}
        for idx, label in enumerate(clustering.labels_):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(idx)
            
        return [
            {
                "cluster_id": label,
                "event_indices": indices,
                "size": len(indices)
            }
            for label, indices in clusters.items()
            if label != -1  # Exclude noise
        ]