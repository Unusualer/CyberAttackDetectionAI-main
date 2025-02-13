import pytest
import numpy as np
from datetime import datetime
from ....app.services.ml.zero_day_detection import ZeroDayDetector
from ....app.schemas.zero_day import ZeroDayDetection
from ....app.core.config import settings

pytestmark = pytest.mark.asyncio

@pytest.fixture
def zero_day_detector():
    return ZeroDayDetector()

@pytest.fixture
def sample_normal_data():
    # Generate normal-looking data
    np.random.seed(42)
    return np.random.normal(0, 1, (100, settings.FEATURE_DIMENSION))

@pytest.fixture
def sample_anomalous_data():
    # Generate anomalous-looking data
    np.random.seed(42)
    base = np.random.normal(0, 1, (10, settings.FEATURE_DIMENSION))
    # Add some anomalous patterns
    base[:, 0] = 10  # Unusual value in first feature
    base[:, 1] = -10  # Unusual value in second feature
    return base

async def test_zero_day_detector_initialization(zero_day_detector):
    """Test that the detector initializes correctly"""
    assert zero_day_detector.isolation_forest is not None
    assert zero_day_detector.autoencoder is not None
    assert zero_day_detector.scaler is not None
    assert zero_day_detector.pca is not None

async def test_zero_day_detection_normal_traffic(
    zero_day_detector,
    sample_normal_data
):
    """Test detection on normal traffic patterns"""
    # Train the detector
    await zero_day_detector.train(sample_normal_data)
    
    # Test on a single normal sample
    test_sample = sample_normal_data[0].reshape(1, -1)
    result = await zero_day_detector.detect_zero_day(test_sample)
    
    assert isinstance(result, dict)
    assert "is_zero_day" in result
    assert "confidence" in result
    assert "anomaly_scores" in result
    assert "details" in result
    
    # Should not detect as zero-day
    assert result["is_zero_day"] is False
    assert result["confidence"] >= 0 and result["confidence"] <= 1

async def test_zero_day_detection_anomalous_traffic(
    zero_day_detector,
    sample_normal_data,
    sample_anomalous_data
):
    """Test detection on anomalous traffic patterns"""
    # Train the detector on normal data
    await zero_day_detector.train(sample_normal_data)
    
    # Test on anomalous sample
    test_sample = sample_anomalous_data[0].reshape(1, -1)
    result = await zero_day_detector.detect_zero_day(test_sample)
    
    # Should detect as zero-day
    assert result["is_zero_day"] is True
    assert result["confidence"] > settings.HIGH_CONFIDENCE_THRESHOLD

async def test_feature_importance(zero_day_detector, sample_normal_data):
    """Test feature importance calculation"""
    # Train the detector
    await zero_day_detector.train(sample_normal_data)
    
    # Get detection result
    test_sample = sample_normal_data[0].reshape(1, -1)
    result = await zero_day_detector.detect_zero_day(test_sample)
    
    # Check feature importance
    feature_importance = result["details"]["feature_importance"]
    assert len(feature_importance) == settings.FEATURE_DIMENSION
    assert sum(feature_importance.values()) == pytest.approx(1.0)

async def test_model_persistence(zero_day_detector, sample_normal_data):
    """Test model saving and loading"""
    # Train and save the model
    await zero_day_detector.train(sample_normal_data)
    zero_day_detector.save()
    
    # Create new instance and load the model
    new_detector = ZeroDayDetector()
    
    # Test detection with loaded model
    test_sample = sample_normal_data[0].reshape(1, -1)
    result = await new_detector.detect_zero_day(test_sample)
    
    assert isinstance(result, dict)
    assert "is_zero_day" in result

async def test_detection_performance(
    zero_day_detector,
    sample_normal_data,
    sample_anomalous_data
):
    """Test detection performance metrics"""
    # Train the detector
    await zero_day_detector.train(sample_normal_data)
    
    # Test on multiple samples
    normal_results = []
    for sample in sample_normal_data[:10]:
        result = await zero_day_detector.detect_zero_day(sample.reshape(1, -1))
        normal_results.append(result["is_zero_day"])
    
    anomaly_results = []
    for sample in sample_anomalous_data:
        result = await zero_day_detector.detect_zero_day(sample.reshape(1, -1))
        anomaly_results.append(result["is_zero_day"])
    
    # Calculate metrics
    false_positive_rate = sum(normal_results) / len(normal_results)
    detection_rate = sum(anomaly_results) / len(anomaly_results)
    
    # Check performance thresholds
    assert false_positive_rate <= settings.MAX_FALSE_POSITIVE_RATE
    assert detection_rate >= 0.8  # At least 80% detection rate

async def test_invalid_input_handling(zero_day_detector):
    """Test handling of invalid inputs"""
    with pytest.raises(ValueError):
        await zero_day_detector.detect_zero_day(np.zeros((1, settings.FEATURE_DIMENSION + 1)))
    
    with pytest.raises(ValueError):
        await zero_day_detector.train(np.zeros((10, settings.FEATURE_DIMENSION + 1)))

async def test_confidence_scoring(
    zero_day_detector,
    sample_normal_data,
    sample_anomalous_data
):
    """Test confidence score calculation"""
    # Train the detector
    await zero_day_detector.train(sample_normal_data)
    
    # Get confidence scores for normal and anomalous data
    normal_sample = sample_normal_data[0].reshape(1, -1)
    normal_result = await zero_day_detector.detect_zero_day(normal_sample)
    
    anomalous_sample = sample_anomalous_data[0].reshape(1, -1)
    anomalous_result = await zero_day_detector.detect_zero_day(anomalous_sample)
    
    # Anomalous data should have higher confidence in detection
    assert anomalous_result["confidence"] > normal_result["confidence"]
    
async def test_detection_details(zero_day_detector, sample_normal_data):
    """Test the details provided in detection results"""
    # Train the detector
    await zero_day_detector.train(sample_normal_data)
    
    # Get detection details
    test_sample = sample_normal_data[0].reshape(1, -1)
    result = await zero_day_detector.detect_zero_day(test_sample)
    
    # Check structure of details
    assert "reconstruction_analysis" in result["details"]
    assert "autoencoder_diff" in result["details"]["reconstruction_analysis"]
    assert "pca_diff" in result["details"]["reconstruction_analysis"]
    assert isinstance(result["details"]["timestamp"], str) 