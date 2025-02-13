from pydantic_settings import BaseSettings
from typing import List, Optional, Dict
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-powered Cyber Attack Detection"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    environment: str = "development"
    log_level: str = "INFO"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:123@localhost:5432/cyber_defense"
    ASYNC_DATABASE_URL: Optional[str] = None
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # ML Settings
    MODEL_PATH: str = "models"
    MAX_SEQUENCE_LENGTH: int = 512
    TRAINING_BATCH_SIZE: int = 32
    clustering_distance: float = 0.5
    min_cluster_size: int = 3
    
    # Monitoring
    PROMETHEUS_PORT: int = 9090
    GRAFANA_PORT: int = 3000
    monitoring_interval: int = 60
    cpu_threshold: int = 80
    memory_threshold: int = 85
    response_time_threshold: float = 2.0
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    ML_RATE_LIMIT_PER_MINUTE: int = 10
    high_frequency_threshold: int = 100
    report_cache_ttl: int = 3600
    
    # Security Integration
    security_firewall_url: str = "https://firewall-api/v1"
    security_firewall_api_key: str = "firewall-api-key"
    security_ids_url: str = "https://ids-api/v1"
    security_ids_api_key: str = "ids-api-key"
    security_waf_url: str = "https://waf-api/v1"
    security_waf_api_key: str = "waf-api-key"
    
    # User Management
    first_superuser: str = "admin@example.com"
    first_superuser_password: str = "change-this-password"
    default_api_key: str = "generate-a-secure-api-key"
    
    # SSL
    ssl_cert_path: str = "/etc/ssl/certs/cyber-defense.crt"
    ssl_key_path: str = "/etc/ssl/private/cyber-defense.key"
    
    # Backup
    BACKUP_BUCKET: Optional[str] = None
    AWS_ACCESS_KEY: Optional[str] = None
    AWS_SECRET_KEY: Optional[str] = None
    AWS_REGION: Optional[str] = None
    
    # Integration
    SIEM_URL: Optional[str] = None
    SIEM_API_KEY: Optional[str] = None
    
    # Zero-day Detection Settings
    FEATURE_DIMENSION: int = 50
    ZERO_DAY_THRESHOLD: float = 0.85
    HIGH_CONFIDENCE_THRESHOLD: float = 0.9
    MODEL_RETRAINING_INTERVAL: int = 24  # hours
    
    # Model Parameters
    AUTOENCODER_LAYERS: List[int] = [128, 64, 32, 64, 128]
    ISOLATION_FOREST_ESTIMATORS: int = 200
    ISOLATION_FOREST_CONTAMINATION: float = 0.01
    PCA_VARIANCE_THRESHOLD: float = 0.95
    
    # Alert Settings
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
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()