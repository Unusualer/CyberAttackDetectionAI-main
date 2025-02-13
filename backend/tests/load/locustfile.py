from locust import HttpUser, task, between
import json
import random

class LoadTestUser(HttpUser):
    wait_time = between(0.1, 1.0)
    
    def on_start(self):
        """Login at start"""
        self.login()
        
    def login(self):
        """Authenticate user"""
        response = self.client.post("/api/v1/auth/login", json={
            "username": "test@example.com",
            "password": "testpassword"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
        
    @task(4)
    def detect_threat(self):
        """Simulate threat detection requests"""
        event = self._generate_random_event()
        self.client.post(
            "/api/v1/threats/detect",
            json=event,
            headers=self.headers
        )
        
    @task(2)
    def get_metrics(self):
        """Get monitoring metrics"""
        self.client.get(
            "/api/v1/monitoring/metrics",
            headers=self.headers
        )
        
    @task(1)
    def get_health(self):
        """Check system health"""
        self.client.get("/health")
        
    def _generate_random_event(self):
        """Generate random test event"""
        return {
            "source_ip": f"192.168.1.{random.randint(1, 255)}",
            "destination_ip": f"10.0.0.{random.randint(1, 255)}",
            "protocol": random.choice(["TCP", "UDP", "HTTP"]),
            "bytes_sent": random.randint(1000, 100000),
            "port": random.randint(1, 65535),
            "duration": random.randint(1, 3600)
        } 