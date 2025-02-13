import os
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional
from pathlib import Path
import joblib
import mlflow
import optuna
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier
from sklearn.feature_selection import SelectFromModel
from data_manager import DataManager

class ModelTrainingPipeline:
    def __init__(self, data_manager: DataManager):
        """Initialize the training pipeline with a data manager."""
        self.data_manager = data_manager
        self.models = {}
        self.best_params = {}
        self.feature_selector = None
        
        # Set up MLflow tracking
        mlflow.set_tracking_uri("file:./mlruns")
        
    def optimize_hyperparameters(self, X_train: np.ndarray, y_train: np.ndarray) -> Dict:
        """Optimize XGBoost hyperparameters using Optuna."""
        def objective(trial):
            params = {
                'max_depth': trial.suggest_int('max_depth', 3, 10),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
                'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
                'min_child_weight': trial.suggest_int('min_child_weight', 1, 7),
                'gamma': trial.suggest_float('gamma', 0, 1),
                'subsample': trial.suggest_float('subsample', 0.6, 1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
                'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
                'reg_lambda': trial.suggest_float('reg_lambda', 0, 1),
                'random_state': 42
            }
            
            model = XGBClassifier(**params)
            model.fit(X_train, y_train)
            return model.score(X_train, y_train)
            
        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=50)
        
        return study.best_params
        
    def select_features(self, X_train: np.ndarray, y_train: np.ndarray) -> np.ndarray:
        """Select important features using XGBoost feature importance."""
        if self.feature_selector is None:
            base_model = XGBClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
            self.feature_selector = SelectFromModel(base_model, prefit=False)
            self.feature_selector.fit(X_train, y_train)
            
        return self.feature_selector.transform(X_train)
        
    def train_models(self) -> None:
        """Train the XGBoost model with optimized hyperparameters."""
        # Get training data
        train_data, test_data = self.data_manager.get_training_data()
        
        # Prepare features and labels
        X_train = train_data.drop(['is_attack', 'attack_type', 'level'], axis=1, errors='ignore')
        y_train = train_data['is_attack']
        X_test = test_data.drop(['is_attack', 'attack_type', 'level'], axis=1, errors='ignore')
        y_test = test_data['is_attack']
        
        # Select important features
        X_train_selected = self.select_features(X_train, y_train)
        X_test_selected = self.feature_selector.transform(X_test)
        
        # Train XGBoost with optimized hyperparameters
        with mlflow.start_run(run_name="xgboost_training"):
            best_params = self.optimize_hyperparameters(X_train_selected, y_train)
            model = XGBClassifier(**best_params)
            model.fit(X_train_selected, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test_selected)
            
            # Calculate metrics
            metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred),
                "recall": recall_score(y_test, y_pred),
                "f1_score": f1_score(y_test, y_pred)
            }
            
            # Log metrics and parameters
            mlflow.log_metrics(metrics)
            mlflow.log_params(best_params)
            
            # Save feature importance plot
            feature_importance = pd.DataFrame({
                'feature': X_train.columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            # Save the model
            self.models["xgboost"] = model
            self.best_params["xgboost"] = best_params
            joblib.dump(model, self.data_manager.get_model_path("xgboost"))
            joblib.dump(self.feature_selector, self.data_manager.get_model_path("feature_selector"))
            
    def load_models(self) -> None:
        """Load trained models if they exist."""
        model_path = self.data_manager.get_model_path("xgboost")
        selector_path = self.data_manager.get_model_path("feature_selector")
        
        if model_path.exists():
            self.models["xgboost"] = joblib.load(model_path)
        if selector_path.exists():
            self.feature_selector = joblib.load(selector_path)
            
    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Make predictions using the trained model."""
        if not self.models or "xgboost" not in self.models:
            self.load_models()
            
        if "xgboost" not in self.models:
            raise ValueError("Model not trained yet. Please train the model first.")
            
        # Prepare features
        X = data.drop(['is_attack', 'attack_type', 'level'], axis=1, errors='ignore')
        X_selected = self.feature_selector.transform(X)
        
        return self.models["xgboost"].predict(X_selected)
        
    def evaluate_model(self, test_data: Optional[pd.DataFrame] = None) -> Dict:
        """Evaluate model performance on test data."""
        if test_data is None:
            _, test_data = self.data_manager.get_training_data()
            
        X_test = test_data.drop(['is_attack', 'attack_type', 'level'], axis=1, errors='ignore')
        y_test = test_data['is_attack']
        
        X_test_selected = self.feature_selector.transform(X_test)
        y_pred = self.models["xgboost"].predict(X_test_selected)
        
        return {
            "classification_report": classification_report(y_test, y_pred),
            "confusion_matrix": confusion_matrix(y_test, y_pred),
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred)
        }