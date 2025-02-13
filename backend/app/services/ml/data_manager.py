import os
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

class DataManager:
    def __init__(self, base_path: str = "data"):
        """Initialize the DataManager with paths for data storage."""
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / "raw"
        self.processed_path = self.base_path / "processed"
        self.models_path = Path("models") / "pretrained"
        
        # Create directories if they don't exist
        for path in [self.raw_path, self.processed_path, self.models_path]:
            path.mkdir(parents=True, exist_ok=True)
            
        self.label_encoders = {}
        self.scaler = MinMaxScaler()
        
    def download_nsl_kdd(self) -> None:
        """Download the NSL-KDD dataset if not already present."""
        import requests
        
        train_url = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt"
        test_url = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest%2B.txt"
        
        train_file = self.raw_path / "KDDTrain+.txt"
        test_file = self.raw_path / "KDDTest+.txt"
        
        if not train_file.exists():
            response = requests.get(train_url)
            with open(train_file, 'wb') as f:
                f.write(response.content)
                
        if not test_file.exists():
            response = requests.get(test_url)
            with open(test_file, 'wb') as f:
                f.write(response.content)
                
    def load_nsl_kdd(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load and preprocess the NSL-KDD dataset."""
        # Column names for the dataset
        columns = [
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes',
            'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
            'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
            'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
            'num_access_files', 'num_outbound_cmds', 'is_host_login',
            'is_guest_login', 'count', 'srv_count', 'serror_rate',
            'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
            'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
            'dst_host_srv_count', 'dst_host_same_srv_rate',
            'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
            'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
            'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
            'dst_host_srv_rerror_rate', 'attack_type', 'level'
        ]
        
        # Load the datasets
        train_data = pd.read_csv(self.raw_path / "KDDTrain+.txt", names=columns)
        test_data = pd.read_csv(self.raw_path / "KDDTest+.txt", names=columns)
        
        # Preprocess the data
        train_data = self._preprocess_nsl_kdd(train_data, is_training=True)
        test_data = self._preprocess_nsl_kdd(test_data, is_training=False)
        
        return train_data, test_data
        
    def _preprocess_nsl_kdd(self, data: pd.DataFrame, is_training: bool = True) -> pd.DataFrame:
        """Preprocess the NSL-KDD dataset."""
        # Create binary labels (normal vs attack)
        data['is_attack'] = (data['attack_type'] != 'normal').astype(int)
        
        # Encode categorical features
        categorical_features = ['protocol_type', 'service', 'flag']
        for feature in categorical_features:
            if is_training:
                self.label_encoders[feature] = LabelEncoder()
                data[feature] = self.label_encoders[feature].fit_transform(data[feature])
            else:
                data[feature] = self.label_encoders[feature].transform(data[feature])
                
        # Select features for training
        features = [
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes',
            'dst_bytes', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins',
            'logged_in', 'num_compromised', 'root_shell', 'su_attempted',
            'num_root', 'num_file_creations', 'num_shells', 'num_access_files',
            'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
            'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
            'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
            'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
            'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
            'dst_host_serror_rate', 'dst_host_srv_serror_rate',
            'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
        ]
        
        # Scale numerical features
        if is_training:
            self.scaler.fit(data[features])
        data[features] = self.scaler.transform(data[features])
        
        return data
        
    def get_training_data(self, test_size: float = 0.2, random_state: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Get or generate training and testing data."""
        train_file = self.processed_path / "train_data.csv"
        test_file = self.processed_path / "test_data.csv"
        
        if not train_file.exists() or not test_file.exists():
            # Download and load NSL-KDD dataset
            self.download_nsl_kdd()
            train_data, test_data = self.load_nsl_kdd()
            
            # Save the processed data
            train_data.to_csv(train_file, index=False)
            test_data.to_csv(test_file, index=False)
        else:
            train_data = pd.read_csv(train_file)
            test_data = pd.read_csv(test_file)
            
        return train_data, test_data
        
    def get_model_path(self, model_name: str) -> Path:
        """Get the path for a specific model."""
        return self.models_path / f"{model_name}.pkl" 