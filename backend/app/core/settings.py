from typing import Dict, List
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Cyber Attack Detection AI"
    
    # Security Settings
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Settings
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    # ML Model Settings
    MODEL_PATH: str = "models"
    FEATURE_DIMENSION: int = 50
    ZERO_DAY_THRESHOLD: float = 0.85
    HIGH_CONFIDENCE_THRESHOLD: float = 0.9
    MODEL_RETRAINING_INTERVAL: int = 24  # hours
    USE_GPU: bool = False  # Set to False for CPU-only usage
    
    # Model Architecture (CPU-optimized)
    AUTOENCODER_LAYERS: List[int] = [64, 32, 16, 32, 64]  # Smaller network
    ISOLATION_FOREST_ESTIMATORS: int = 100  # Reduced from 200
    ISOLATION_FOREST_CONTAMINATION: float = 0.01
    PCA_VARIANCE_THRESHOLD: float = 0.95
    BATCH_SIZE: int = 32
    MAX_EPOCHS: int = 50
    
    # Performance Settings (CPU-optimized)
    MAX_PROCESSING_TIME: float = 10.0  # Increased for CPU
    PARALLEL_PROCESSING_THRESHOLD: int = 50  # Reduced for CPU
    NUM_WORKERS: int = 4  # Number of CPU workers
    
    # Alert Configuration
    ALERT_SEVERITY_THRESHOLDS: Dict[str, float] = {
        "low": 0.7,
        "medium": 0.8,
        "high": 0.9,
        "critical": 0.95
    }
    
    # Response Settings
    AUTOMATED_RESPONSE_THRESHOLD: float = 0.95
    MAX_FALSE_POSITIVE_RATE: float = 0.01
    INCIDENT_ESCALATION_THRESHOLD: float = 0.9
    
    # Performance Settings
    MAX_PROCESSING_TIME: float = 5.0  # seconds
    BATCH_SIZE: int = 32
    PARALLEL_PROCESSING_THRESHOLD: int = 100  # events
    
    # Monitoring Settings
    PERFORMANCE_MONITORING_INTERVAL: int = 60  # seconds
    METRICS_RETENTION_PERIOD: int = 90  # days
    ALERT_RETENTION_PERIOD: int = 180  # days
    
    # SIEM Integration
    SIEM_URL: str = Field(None, env="SIEM_URL")
    SIEM_API_KEY: str = Field(None, env="SIEM_API_KEY")
    
    # Notification Settings
    ENABLE_EMAIL_NOTIFICATIONS: bool = True
    ENABLE_SLACK_NOTIFICATIONS: bool = False
    NOTIFICATION_COOLDOWN: int = 300  # seconds
    
    # Feature Extraction
    NETWORK_FEATURES: List[str] = [
        "bytes_sent",
        "bytes_received",
        "packets_sent",
        "packets_received",
        "duration",
        "protocol",
        "port",
        "flags"
    ]
    
    SYSTEM_FEATURES: List[str] = [
        "cpu_usage",
        "memory_usage",
        "disk_io",
        "network_connections",
        "process_count",
        "system_calls"
    ]
    
    USER_FEATURES: List[str] = [
        "login_attempts",
        "command_frequency",
        "resource_access",
        "privilege_changes",
        "file_operations"
    ]
    
    # Model Versioning
    ENABLE_MODEL_VERSIONING: bool = True
    MAX_MODEL_VERSIONS: int = 5
    MODEL_BACKUP_INTERVAL: int = 24  # hours
    
    # Feature Processing
    ENABLE_FEATURE_SELECTION: bool = True  # Reduce dimensionality
    MAX_FEATURES: int = 30  # Limit number of features
    FEATURE_SELECTION_METHOD: str = "variance"  # Options: variance, mutual_info
    
    # Batch Processing
    ENABLE_BATCH_PROCESSING: bool = True
    MAX_BATCH_SIZE: int = 1000
    MIN_BATCH_SIZE: int = 32
    
    class Config:
        env_file = ".env"
        case_sensitive = True 