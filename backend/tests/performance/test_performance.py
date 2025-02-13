import pytest
import asyncio
import time
from locust import HttpUser, task, between
from ...app.core.config import settings
from ...app.services.threat_analysis import ThreatAnalysisService
from ...app.services.ml.anomaly_detection import AnomalyDetector

class ThreatDetectionPerformance:
    def __init__(self):
        self.threat_analyzer = ThreatAnalysisService()
        self.anomaly_detector = AnomalyDetector()

    async def measure_detection_time(self, event):
        start_time = time.time()
        result = await self.threat_analyzer.analyze_event(event)
        end_time = time.time()
        return end_time - start_time, result

    async def measure_model_inference(self, data):
        start_time = time.time()
        prediction = self.anomaly_detector.predict(data)
        end_time = time.time()
        return end_time - start_time, prediction

class ThreatAPIUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def test_threat_detection(self):
        test_event = {
            "source_ip": "192.168.1.100",
            "destination_ip": "10.0.0.2",
            "timestamp": "2023-11-22T10:00:00Z",
            "protocol": "TCP",
            "bytes_sent": 15000,
            "port": 445,
            "duration": 120,
            "packets": 150
        }
        
        with self.client.post(
            f"{settings.API_V1_STR}/threats/detect",
            json=test_event,
            catch_response=True
        ) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Failed with status code: {response.status_code}")

    @task(2)
    def test_get_threat_summary(self):
        with self.client.get(
            f"{settings.API_V1_STR}/threats/summary",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code: {response.status_code}") 