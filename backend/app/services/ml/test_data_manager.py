import os
import pandas as pd
from pathlib import Path
from data_manager import DataManager

def test_data_manager():
    """Test the DataManager functionality."""
    # Initialize DataManager
    data_manager = DataManager()
    
    # Test directory creation
    assert data_manager.raw_path.exists(), "Raw data directory not created"
    assert data_manager.processed_path.exists(), "Processed data directory not created"
    assert data_manager.models_path.exists(), "Models directory not created"
    
    # Test attack patterns
    patterns = data_manager.get_attack_patterns()
    assert "dos_attack" in patterns, "DoS attack pattern not found"
    assert "brute_force" in patterns, "Brute force attack pattern not found"
    
    # Test data generation
    data = data_manager.generate_sample_data(n_samples=100)
    assert len(data) == 100, "Generated data size mismatch"
    assert "is_attack" in data.columns, "Attack label column missing"
    assert "attack_type" in data.columns, "Attack type column missing"
    
    # Test training data split
    train_data, test_data = data_manager.get_training_data(test_size=0.2)
    assert isinstance(train_data, pd.DataFrame), "Training data not a DataFrame"
    assert isinstance(test_data, pd.DataFrame), "Test data not a DataFrame"
    
    # Test adding new labeled data
    new_data = data_manager.generate_sample_data(n_samples=50)
    data_manager.add_labeled_data(new_data)
    
    # Test model path generation
    model_path = data_manager.get_model_path("test_model")
    assert str(model_path).endswith(".pkl"), "Invalid model file extension"
    
    print("All tests passed successfully!")

if __name__ == "__main__":
    test_data_manager() 