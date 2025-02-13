import numpy as np
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)

def generate_sample_data(n_normal: int = 1000, n_attacks: int = 200) -> pd.DataFrame:
    """Generate sample dataset with normal and attack patterns"""
    # Generate normal traffic
    normal_data = []
    for _ in range(n_normal):
        event = {
            # Network features
            "bytes_sent": np.random.normal(5000, 1000),
            "bytes_received": np.random.normal(8000, 1500),
            "packets_sent": np.random.normal(50, 10),
            "packets_received": np.random.normal(80, 15),
            "protocol": np.random.choice(["tcp", "udp", "http"]),
            "port": np.random.choice([80, 443, 22, 53]),
            
            # System features
            "cpu_usage": np.random.normal(30, 5),
            "memory_usage": np.random.normal(60, 10),
            "disk_io": np.random.normal(5000, 1000),
            "process_count": np.random.normal(200, 20),
            
            # User features
            "login_attempts": np.random.poisson(2),
            "file_operations": np.random.normal(100, 20),
            
            "is_attack": 0,
            "timestamp": datetime.now().isoformat()
        }
        normal_data.append(event)
        
    # Generate attack patterns
    attack_data = []
    attack_types = ["dos", "brute_force", "data_exfil", "malware"]
    
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
        elif attack_type == "data_exfil":
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
        else:  # malware
            event = {
                "bytes_sent": np.random.normal(15000, 2000),
                "bytes_received": np.random.normal(12000, 1800),
                "packets_sent": np.random.normal(200, 30),
                "packets_received": np.random.normal(150, 25),
                "protocol": np.random.choice(["tcp", "udp", "http"]),
                "port": np.random.randint(1024, 65535),
                "cpu_usage": np.random.normal(70, 10),
                "memory_usage": np.random.normal(75, 8),
                "disk_io": np.random.normal(20000, 2000),
                "process_count": np.random.normal(300, 30),
                "login_attempts": np.random.poisson(5),
                "file_operations": np.random.normal(300, 30)
            }
            
        event["is_attack"] = 1
        event["attack_type"] = attack_type
        event["timestamp"] = datetime.now().isoformat()
        attack_data.append(event)
        
    # Combine and shuffle
    all_data = pd.DataFrame(normal_data + attack_data)
    return all_data.sample(frac=1).reset_index(drop=True)

def get_attack_signatures() -> Dict[str, Any]:
    """Get predefined attack signatures"""
    return {
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
        },
        "malware": {
            "description": "Malware activity pattern",
            "indicators": {
                "unusual_process": "new_process_count > baseline",
                "network_scan": "unique_ports > threshold",
                "suspicious_connections": "unknown_destinations > 0"
            },
            "severity": "critical"
        }
    }

def get_baseline_metrics() -> Dict[str, Any]:
    """Get baseline metrics for normal system behavior"""
    return {
        "network": {
            "avg_bytes_per_second": 5000,
            "avg_packets_per_second": 50,
            "common_ports": [80, 443, 22, 53],
            "normal_protocols": ["tcp", "udp", "http", "https", "dns"]
        },
        "system": {
            "avg_cpu_usage": 30,
            "avg_memory_usage": 60,
            "avg_disk_io": 5000,
            "avg_process_count": 200
        },
        "user": {
            "avg_login_attempts": 2,
            "avg_file_operations": 100,
            "working_hours": [8, 18]
        }
    }

def save_dataset(data: pd.DataFrame, filename: str):
    """Save dataset to file"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    file_path = data_dir / filename
    data.to_csv(file_path, index=False)
    logger.info(f"Dataset saved to {file_path}")

def load_dataset(filename: str) -> pd.DataFrame:
    """Load dataset from file"""
    file_path = Path("data") / filename
    if not file_path.exists():
        logger.warning(f"Dataset {filename} not found, generating new data")
        data = generate_sample_data()
        save_dataset(data, filename)
        return data
        
    return pd.read_csv(file_path)

def get_training_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Get training and validation datasets"""
    data = load_dataset("security_events.csv")
    
    # Split into train/validation (80/20)
    train_size = int(len(data) * 0.8)
    train_data = data[:train_size]
    val_data = data[train_size:]
    
    return train_data, val_data 