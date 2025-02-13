from typing import Dict, Any, List
import numpy as np
from datetime import datetime, timedelta
from ..schemas.schemas import UserActivity, SystemActivity, BehaviorProfile, BehaviorAlert
from ..core.config import settings
from .ml.anomaly_detection import AnomalyDetector
import logging

logger = logging.getLogger(__name__)

class BehavioralAnalysisService:
    def __init__(self):
        self.anomaly_detector = AnomalyDetector()
        self.behavior_profiles = {}  # Cache of user/system behavior profiles
        
    async def analyze_user_behavior(
        self,
        user_id: str,
        activities: List[UserActivity]
    ) -> List[BehaviorAlert]:
        """Analyze user behavior for anomalies"""
        try:
            # Get or create user behavior profile
            profile = await self._get_behavior_profile(user_id)
            
            # Extract behavioral features
            features = self._extract_user_features(activities)
            
            # Compare against baseline
            anomalies = await self._detect_behavioral_anomalies(
                features,
                profile
            )
            
            # Generate alerts for anomalies
            alerts = []
            for anomaly in anomalies:
                alert = await self._create_behavior_alert(
                    user_id=user_id,
                    anomaly_type=anomaly["type"],
                    severity=anomaly["severity"],
                    evidence=anomaly["evidence"]
                )
                alerts.append(alert)
            
            # Update behavior profile
            await self._update_behavior_profile(user_id, features)
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error in behavioral analysis: {str(e)}")
            raise
            
    def _extract_user_features(self, activities: List[UserActivity]) -> np.ndarray:
        """Extract behavioral features from user activities"""
        features = {
            "login_times": [],
            "accessed_resources": set(),
            "failed_attempts": 0,
            "data_access_volume": 0,
            "unusual_commands": 0,
            "privilege_uses": 0
        }
        
        for activity in activities:
            # Analyze login patterns
            if activity.type == "login":
                features["login_times"].append(activity.timestamp.hour)
                
            # Track resource access
            if activity.type == "resource_access":
                features["accessed_resources"].add(activity.resource_id)
                features["data_access_volume"] += activity.data_volume
                
            # Monitor authentication failures
            if activity.type == "auth_failure":
                features["failed_attempts"] += 1
                
            # Track privileged operations
            if activity.is_privileged:
                features["privilege_uses"] += 1
                
            # Detect unusual commands
            if self._is_unusual_command(activity.command):
                features["unusual_commands"] += 1
                
        return self._normalize_features(features)
        
    async def _detect_behavioral_anomalies(
        self,
        features: np.ndarray,
        profile: BehaviorProfile
    ) -> List[Dict[str, Any]]:
        """Detect anomalies in behavioral features"""
        anomalies = []
        
        # Check for time-based anomalies
        if self._is_unusual_timing(features, profile):
            anomalies.append({
                "type": "unusual_timing",
                "severity": "medium",
                "evidence": self._get_timing_evidence(features, profile)
            })
            
        # Check for excessive failures
        if features["failed_attempts"] > profile.failure_threshold:
            anomalies.append({
                "type": "excessive_failures",
                "severity": "high",
                "evidence": {
                    "failures": features["failed_attempts"],
                    "threshold": profile.failure_threshold
                }
            })
            
        # Check for unusual data access
        if self._is_unusual_data_access(features, profile):
            anomalies.append({
                "type": "unusual_data_access",
                "severity": "high",
                "evidence": self._get_data_access_evidence(features, profile)
            })
            
        # Check for privilege abuse
        if self._is_privilege_abuse(features, profile):
            anomalies.append({
                "type": "privilege_abuse",
                "severity": "critical",
                "evidence": self._get_privilege_evidence(features, profile)
            })
            
        return anomalies
        
    def _is_unusual_timing(
        self,
        features: np.ndarray,
        profile: BehaviorProfile
    ) -> bool:
        """Check if activity timing is unusual"""
        current_hours = set(features["login_times"])
        usual_hours = set(profile.usual_hours)
        
        # Calculate how many activities occurred outside usual hours
        unusual_hours = current_hours - usual_hours
        return len(unusual_hours) > settings.UNUSUAL_HOURS_THRESHOLD
        
    def _is_unusual_data_access(
        self,
        features: np.ndarray,
        profile: BehaviorProfile
    ) -> bool:
        """Check for unusual data access patterns"""
        # Check volume anomalies
        volume_ratio = features["data_access_volume"] / profile.avg_data_volume
        if volume_ratio > settings.DATA_VOLUME_THRESHOLD:
            return True
            
        # Check resource access anomalies
        new_resources = features["accessed_resources"] - profile.usual_resources
        if len(new_resources) > settings.NEW_RESOURCE_THRESHOLD:
            return True
            
        return False
        
    def _is_privilege_abuse(
        self,
        features: np.ndarray,
        profile: BehaviorProfile
    ) -> bool:
        """Check for potential privilege abuse"""
        # Check frequency of privileged operations
        if features["privilege_uses"] > profile.privilege_threshold:
            return True
            
        # Check combination of privileges and unusual timing
        if features["privilege_uses"] > 0 and self._is_unusual_timing(features, profile):
            return True
            
        return False
        
    async def _update_behavior_profile(
        self,
        user_id: str,
        features: np.ndarray
    ) -> None:
        """Update user's behavior profile with new activities"""
        profile = self.behavior_profiles.get(user_id)
        if not profile:
            profile = BehaviorProfile(user_id=user_id)
            
        # Update profile statistics
        profile.update_statistics(features)
        
        # Save updated profile
        self.behavior_profiles[user_id] = profile 