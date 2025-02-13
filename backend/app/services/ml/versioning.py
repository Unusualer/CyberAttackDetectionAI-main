from typing import Dict, Any, Optional
from datetime import datetime
import json
import os
from ...core.config import settings
import logging

logger = logging.getLogger(__name__)

class ModelVersionManager:
    def __init__(self):
        self.version_history = {}
        self.current_versions = {}
        self.model_path = settings.MODEL_PATH
        
    async def register_model_version(
        self,
        model_type: str,
        version: str,
        metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        """Register a new model version"""
        try:
            timestamp = datetime.utcnow()
            
            version_info = {
                "version": version,
                "timestamp": timestamp.isoformat(),
                "metrics": metrics,
                "status": "active"
            }
            
            # Update version history
            if model_type not in self.version_history:
                self.version_history[model_type] = []
            self.version_history[model_type].append(version_info)
            
            # Update current version if metrics are better
            if self._is_better_version(model_type, metrics):
                self.current_versions[model_type] = version_info
                await self._save_model_metadata(model_type, version_info)
                
            return version_info
            
        except Exception as e:
            logger.error(f"Error registering model version: {str(e)}")
            raise
            
    async def get_current_version(self, model_type: str) -> Optional[Dict[str, Any]]:
        """Get current model version info"""
        return self.current_versions.get(model_type)
        
    async def _save_model_metadata(self, model_type: str, version_info: Dict[str, Any]):
        """Save model metadata to disk"""
        metadata_path = os.path.join(
            self.model_path,
            model_type,
            "metadata.json"
        )
        
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
        
        with open(metadata_path, "w") as f:
            json.dump(version_info, f, indent=2)
            
    def _is_better_version(self, model_type: str, new_metrics: Dict[str, float]) -> bool:
        """Check if new version performs better than current"""
        if model_type not in self.current_versions:
            return True
            
        current_metrics = self.current_versions[model_type]["metrics"]
        
        # Compare key metrics
        if new_metrics["accuracy"] > current_metrics["accuracy"]:
            return True
        if new_metrics["f1_score"] > current_metrics["f1_score"]:
            return True
            
        return False