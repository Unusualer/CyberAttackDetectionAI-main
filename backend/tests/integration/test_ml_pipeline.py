import pytest
import numpy as np
from ...app.services.ml.training_pipeline import ModelTrainingPipeline
from ...app.schemas.schemas import TrainingResult

pytestmark = pytest.mark.asyncio

async def test_model_training_pipeline(
    test_db,
    test_anomaly_detector
):
    """Test ML model training pipeline"""
    pipeline = ModelTrainingPipeline()

    # Generate test data
    X_train = np.random.rand(1000, 50)
    y_train = np.random.randint(0, 2, 1000)

    # Train models
    result = await pipeline._train_anomaly_detector({
        "X_train": X_train,
        "X_val": X_train[:100],
        "y_val": y_train[:100]
    })

    # Verify training results
    assert isinstance(result, dict)
    assert "accuracy" in result
    assert "f1_score" in result
    assert result["accuracy"] > 0.5

    # Test model predictions
    test_data = np.random.rand(1, 50)
    prediction = test_anomaly_detector.predict(test_data)
    assert "is_anomaly" in prediction
    assert "anomaly_score" in prediction
    assert isinstance(prediction["is_anomaly"], bool) 