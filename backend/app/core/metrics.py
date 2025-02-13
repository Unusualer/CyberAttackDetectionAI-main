from prometheus_client import Counter, Histogram, Gauge
from typing import Dict, Any

# Threat detection metrics
THREATS_DETECTED = Counter(
    'cyber_defense_threats_detected_total',
    'Total number of threats detected',
    ['severity', 'type']
)

DETECTION_TIME = Histogram(
    'cyber_defense_detection_time_seconds',
    'Time spent processing threat detection',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

# ML model metrics
MODEL_ACCURACY = Gauge(
    'ml_model_accuracy',
    'Current accuracy of ML models',
    ['model_name']
)

MODEL_PREDICTION_TIME = Histogram(
    'ml_model_prediction_time_seconds',
    'Time spent on model inference',
    ['model_name'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0]
)

# System metrics
ACTIVE_CONNECTIONS = Gauge(
    'cyber_defense_active_connections',
    'Number of active agent connections'
)

EVENT_PROCESSING_QUEUE = Gauge(
    'cyber_defense_event_queue_size',
    'Number of events waiting to be processed'
)

class MetricsCollector:
    @staticmethod
    def record_threat_detection(threat_type: str, severity: str):
        THREATS_DETECTED.labels(severity=severity, type=threat_type).inc()

    @staticmethod
    def record_detection_time(duration: float):
        DETECTION_TIME.observe(duration)

    @staticmethod
    def update_model_accuracy(model_name: str, accuracy: float):
        MODEL_ACCURACY.labels(model_name=model_name).set(accuracy)

    @staticmethod
    def record_prediction_time(model_name: str, duration: float):
        MODEL_PREDICTION_TIME.labels(model_name=model_name).observe(duration)

    @staticmethod
    def update_connection_count(count: int):
        ACTIVE_CONNECTIONS.set(count)

    @staticmethod
    def update_event_queue_size(size: int):
        EVENT_PROCESSING_QUEUE.set(size) 