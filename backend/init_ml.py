import numpy as np
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Create directories
Path("data/raw").mkdir(parents=True, exist_ok=True)
Path("data/processed").mkdir(parents=True, exist_ok=True)
Path("models/pretrained").mkdir(parents=True, exist_ok=True)

# Generate sample data
n_normal = 1000
n_attacks = 200

# Normal traffic
normal_data = []
for _ in range(n_normal):
    event = {
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
        "is_attack": 0,
        "timestamp": datetime.now().isoformat()
    }
    normal_data.append(event)

# Attack traffic
attack_data = []
attack_types = ["dos", "brute_force", "data_exfil"]

for _ in range(n_attacks):
    attack_type = np.random.choice(attack_types)
    
    if attack_type == "dos":
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
    else:  # data_exfil
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
    
    event["is_attack"] = 1
    event["attack_type"] = attack_type
    event["timestamp"] = datetime.now().isoformat()
    attack_data.append(event)

# Combine and save data
all_data = pd.DataFrame(normal_data + attack_data)
all_data = all_data.sample(frac=1).reset_index(drop=True)

# Save raw data
all_data.to_csv("data/raw/security_events.csv", index=False)

# Process and save training data
numeric_cols = [
    "bytes_sent", "bytes_received", "packets_sent", "packets_received",
    "cpu_usage", "memory_usage", "disk_io", "process_count",
    "login_attempts", "file_operations"
]

# Scale numeric features
scaler = StandardScaler()
processed_data = all_data.copy()
processed_data[numeric_cols] = scaler.fit_transform(all_data[numeric_cols])

# Save processed data
processed_data.to_csv("data/processed/security_events.csv", index=False)

# Train and save initial model
X = processed_data[numeric_cols].values
iso_forest = IsolationForest(
    n_estimators=100,
    contamination=0.1,
    random_state=42,
    n_jobs=-1
)
iso_forest.fit(X)

# Save models
joblib.dump(scaler, "models/pretrained/scaler.joblib")
joblib.dump(iso_forest, "models/pretrained/isolation_forest.joblib")

# Save attack patterns
attack_patterns = {
    "dos": {
        "description": "Denial of Service attack pattern",
        "indicators": {
            "high_traffic": "packets_per_second > 1000",
            "connection_flood": "concurrent_connections > 100",
            "resource_exhaustion": "cpu_usage > 90 or memory_usage > 90"
        },
        "severity": "high"
    },
    "brute_force": {
        "description": "Brute force login attempt pattern",
        "indicators": {
            "failed_logins": "login_attempts > 10 per minute",
            "single_user": "unique_users == 1",
            "common_services": "port in [22, 3389, 445]"
        },
        "severity": "high"
    },
    "data_exfil": {
        "description": "Data exfiltration pattern",
        "indicators": {
            "large_outbound": "bytes_sent > 100MB",
            "unusual_protocol": "protocol in [ftp, unusual_dns]",
            "sensitive_access": "file_operations > normal_threshold"
        },
        "severity": "critical"
    }
}

with open("data/raw/attack_patterns.json", "w") as f:
    json.dump(attack_patterns, f, indent=2)

print("ML system initialized successfully!")
print(f"Generated {len(normal_data)} normal events and {len(attack_data)} attack events")
print("Models and data saved in the following locations:")
print("- Raw data: data/raw/security_events.csv")
print("- Processed data: data/processed/security_events.csv")
print("- Scaler model: models/pretrained/scaler.joblib")
print("- Isolation Forest model: models/pretrained/isolation_forest.joblib")
print("- Attack patterns: data/raw/attack_patterns.json") 