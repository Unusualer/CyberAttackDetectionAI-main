import os
import numpy as np
import pandas as pd
from pathlib import Path
from data_manager import DataManager
from training_pipeline import ModelTrainingPipeline

def test_training_pipeline():
    """Test the ModelTrainingPipeline functionality."""
    # Initialize DataManager and ModelTrainingPipeline
    data_manager = DataManager()
    pipeline = ModelTrainingPipeline(data_manager)
    
    # Test data loading and preprocessing
    train_data, test_data = data_manager.get_training_data()
    assert isinstance(train_data, pd.DataFrame), "Training data not loaded correctly"
    assert isinstance(test_data, pd.DataFrame), "Test data not loaded correctly"
    
    # Test feature selection
    X_train = train_data.drop(['is_attack', 'attack_type', 'level'], axis=1, errors='ignore')
    y_train = train_data['is_attack']
    X_selected = pipeline.select_features(X_train, y_train)
    assert isinstance(X_selected, np.ndarray), "Feature selection failed"
    
    # Test model training
    pipeline.train_models()
    assert "xgboost" in pipeline.models, "XGBoost model not trained"
    assert pipeline.feature_selector is not None, "Feature selector not created"
    
    # Test prediction
    X_test = test_data.drop(['is_attack', 'attack_type', 'level'], axis=1, errors='ignore')
    predictions = pipeline.predict(X_test)
    assert len(predictions) == len(X_test), "Incorrect number of predictions"
    assert all(isinstance(pred, (np.int64, int)) for pred in predictions), "Invalid prediction values"
    
    # Test model evaluation
    eval_results = pipeline.evaluate_model(test_data)
    assert "accuracy" in eval_results, "Missing accuracy in evaluation results"
    assert "precision" in eval_results, "Missing precision in evaluation results"
    assert "recall" in eval_results, "Missing recall in evaluation results"
    assert "f1_score" in eval_results, "Missing F1-score in evaluation results"
    
    print("All tests passed successfully!")

if __name__ == "__main__":
    test_training_pipeline() 