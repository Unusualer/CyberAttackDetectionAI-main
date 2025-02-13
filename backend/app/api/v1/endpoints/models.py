from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ....schemas.ml import ModelInfo, TrainingConfig
from ....services.ml.training_pipeline import ModelTrainingPipeline
from ....api import deps

router = APIRouter()

@router.get("/models", response_model=List[ModelInfo])
async def get_models(
    current_user = Depends(deps.get_current_active_superuser)
):
    """Get all ML models information"""
    pipeline = ModelTrainingPipeline()
    return await pipeline.get_models_info()

@router.post("/models/train")
async def train_model(
    config: TrainingConfig,
    current_user = Depends(deps.get_current_active_superuser)
):
    """Trigger model training"""
    pipeline = ModelTrainingPipeline()
    return await pipeline.start_training(config) 