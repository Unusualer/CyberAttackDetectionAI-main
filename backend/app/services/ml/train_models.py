from data_manager import DataManager
from training_pipeline import ModelTrainingPipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Train and evaluate ML models for cyber attack detection."""
    try:
        # Initialize data manager and training pipeline
        data_manager = DataManager()
        pipeline = ModelTrainingPipeline(data_manager)
        
        logger.info("Generating sample data...")
        # Generate sample data
        df = data_manager.generate_sample_data(n_samples=10000)
        
        logger.info("Preprocessing data...")
        # Preprocess data
        X, y = data_manager.preprocess_data(df)
        
        # Split data into train and test sets
        logger.info("Splitting data into train and test sets...")
        X_train, X_test, y_train, y_test = data_manager.split_data(X, y)
        
        # Train anomaly detector
        logger.info("Training anomaly detector...")
        pipeline.train_anomaly_detector(X_train)
        
        # Train threat classifier
        logger.info("Training threat classifier...")
        pipeline.train_threat_classifier(X_train, y_train, optimize=True)
        
        # Evaluate models
        logger.info("Evaluating models...")
        metrics = pipeline.evaluate_models(X_test, y_test)
        
        # Log metrics
        logger.info("Logging metrics...")
        pipeline.log_metrics(metrics)
        
        # Save models
        logger.info("Saving models...")
        pipeline.save_models()
        
        # Print evaluation results
        logger.info("Evaluation Results:")
        for model_name, model_metrics in metrics.items():
            logger.info(f"\n{model_name} Results:")
            logger.info(f"Classification Report:\n{model_metrics['classification_report']}")
            logger.info(f"Confusion Matrix:\n{model_metrics['confusion_matrix']}")
        
        logger.info("Training completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during training: {str(e)}")
        raise

if __name__ == "__main__":
    main() 