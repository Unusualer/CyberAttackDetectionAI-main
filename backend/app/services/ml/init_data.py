import numpy as np
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def create_directories():
    """Create necessary directories if they don't exist"""
    dirs = [
        "backend/data/raw",
        "backend/data/processed",
        "backend/models/pretrained"
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

def create_attack_patterns():
    """Create and save attack patterns"""
    patterns = {
        "dos_attack": {
            "features": {
                "packets_per_second": ">1000",
                "unique_ips": "<3",
                "protocol": "tcp/udp",
                "port_range": "common_ports"
            },
            "severity": "high",
            "description": "Denial of Service attack pattern"
        },
        "brute_force": {
            "features": {
                "login_attempts": ">10/minute",
                "failed_ratio": ">0.8",
                "source_ip": "single",
                "target_service": "ssh/rdp/web"
            },
            "severity": "high",
            "description": "Brute force attack pattern"
        },
        "data_exfiltration": {
            "features": {
                "bytes_out": ">normal_threshold",
                "destination": "external",
                "time_window": "off_hours",
                "protocol": "http/ftp/dns"
            },
            "severity": "critical",
            "description": "Data exfiltration pattern"
        }
    }
    
    with open("backend/data/raw/attack_patterns.json", "w") as f:
        json.dump(patterns, f, indent=2)

def generate_normal_traffic(n_samples=1000):
    """Generate normal network traffic data"""
    timestamps = [
        datetime.now() - timedelta(hours=x)
        for x in np.random.uniform(0, 168, n_samples)  # Last week
    ]
    
    data = []
    for ts in timestamps:
        event = {
            "timestamp": ts.isoformat(),
            "bytes_sent": np.random.normal(5000, 1000),
            "bytes_received": np.random.normal(8000, 1500),
            "packets_sent": np.random.normal(50, 10),
            "packets_received": np.random.normal(80, 15),
            "protocol": np.random.choice(["tcp", "udp", "http"]),
            "port": np.random.choice([80, 443, 22, 53]),
            "cpu_usage": np.random.normal(30, 5),
            "memory_usage": np.random.normal(60, 10),
            "disk_io": np.random.normal(5000, 1000),
            "process_count": np.random.normal(200, 20),
            "login_attempts": np.random.poisson(2),
            "file_operations": np.random.normal(100, 20),
            "is_attack": 0
        }
        data.append(event)
    
    return pd.DataFrame(data)

def generate_attack_traffic(n_samples=200):
    """Generate attack traffic data"""
    timestamps = [
        datetime.now() - timedelta(hours=x)
        for x in np.random.uniform(0, 168, n_samples)
    ]
    
    attack_types = ["dos_attack", "brute_force", "data_exfiltration"]
    data = []
    
    for ts in timestamps:
        attack_type = np.random.choice(attack_types)
        
        if attack_type == "dos_attack":
            event = {
                "bytes_sent": np.random.normal(50000, 5000),
                "bytes_received": np.random.normal(80000, 8000),
                "packets_sent": np.random.normal(1500, 100),
                "packets_received": np.random.normal(2000, 150),
                "protocol": np.random.choice(["tcp", "udp"]),
                "port": np.random.choice([80, 443]),
                "cpu_usage": np.random.normal(90, 5),
                "memory_usage": np.random.normal(85, 5),
                "disk_io": np.random.normal(50000, 5000),
                "process_count": np.random.normal(500, 50),
                "login_attempts": np.random.poisson(2),
                "file_operations": np.random.normal(100, 20)
            }
        elif attack_type == "brute_force":
            event = {
                "bytes_sent": np.random.normal(1000, 200),
                "bytes_received": np.random.normal(500, 100),
                "packets_sent": np.random.normal(100, 20),
                "packets_received": np.random.normal(50, 10),
                "protocol": "tcp",
                "port": np.random.choice([22, 3389]),
                "cpu_usage": np.random.normal(40, 5),
                "memory_usage": np.random.normal(70, 5),
                "disk_io": np.random.normal(8000, 1000),
                "process_count": np.random.normal(250, 20),
                "login_attempts": np.random.normal(50, 10),
                "file_operations": np.random.normal(20, 5)
            }
        else:  # data_exfiltration
            event = {
                "bytes_sent": np.random.normal(100000, 10000),
                "bytes_received": np.random.normal(5000, 1000),
                "packets_sent": np.random.normal(1000, 100),
                "packets_received": np.random.normal(50, 10),
                "protocol": np.random.choice(["ftp", "http"]),
                "port": np.random.choice([20, 21, 80, 443]),
                "cpu_usage": np.random.normal(50, 5),
                "memory_usage": np.random.normal(65, 5),
                "disk_io": np.random.normal(100000, 10000),
                "process_count": np.random.normal(220, 20),
                "login_attempts": np.random.poisson(3),
                "file_operations": np.random.normal(500, 50)
            }
        
        event["timestamp"] = ts.isoformat()
        event["is_attack"] = 1
        event["attack_type"] = attack_type
        data.append(event)
    
    return pd.DataFrame(data)

def create_initial_dataset():
    """Create and save initial dataset"""
    normal_data = generate_normal_traffic()
    attack_data = generate_attack_traffic()
    
    # Combine and shuffle
    all_data = pd.concat([normal_data, attack_data])
    all_data = all_data.sample(frac=1).reset_index(drop=True)
    
    # Save raw data
    all_data.to_csv("backend/data/raw/security_events.csv", index=False)
    
    # Process and save training data
    scaler = StandardScaler()
    numeric_cols = [
        "bytes_sent", "bytes_received", "packets_sent", "packets_received",
        "cpu_usage", "memory_usage", "disk_io", "process_count",
        "login_attempts", "file_operations"
    ]
    
    processed_data = all_data.copy()
    processed_data[numeric_cols] = scaler.fit_transform(all_data[numeric_cols])
    
    # Save processed data and scaler
    processed_data.to_csv("backend/data/processed/security_events.csv", index=False)
    joblib.dump(scaler, "backend/models/pretrained/scaler.joblib")

def train_initial_models():
    """Train and save initial models"""
    # Load processed data
    data = pd.read_csv("backend/data/processed/security_events.csv")
    
    # Prepare features
    feature_cols = [
        "bytes_sent", "bytes_received", "packets_sent", "packets_received",
        "cpu_usage", "memory_usage", "disk_io", "process_count",
        "login_attempts", "file_operations"
    ]
    X = data[feature_cols].values
    
    # Train isolation forest for anomaly detection
    iso_forest = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42,
        n_jobs=-1
    )
    iso_forest.fit(X)
    
    # Save model
    joblib.dump(iso_forest, "backend/models/pretrained/isolation_forest.joblib")

def initialize_ml_system():
    """Initialize the entire ML system"""
    print("Creating directories...")
    create_directories()
    
    print("Creating attack patterns...")
    create_attack_patterns()
    
    print("Creating initial dataset...")
    create_initial_dataset()
    
    print("Training initial models...")
    train_initial_models()
    
    print("ML system initialized successfully!")

if __name__ == "__main__":
    initialize_ml_system() 