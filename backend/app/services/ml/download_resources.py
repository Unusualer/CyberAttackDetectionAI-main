import os
from pathlib import Path
import kaggle
from transformers import AutoTokenizer, AutoModel
import requests
import zipfile
import logging
import torch

logger = logging.getLogger(__name__)

KAGGLE_DATASETS = {
    "nsl-kdd": "hassan06/nslkdd",
    "cicids2017": "cicdataset/cicids2017",
    "system-logs": "gyulukeyi/system-logs",
    "malware-detection": "nsaravana/malware-detection"
}

HUGGINGFACE_MODELS = {
    "security-bert": "microsoft/security-bert",
    "anomaly-transformer": "facebook/bart-large",
    "log-analyzer": "bert-base-uncased"
}

def setup_kaggle():
    """Setup Kaggle credentials"""
    os.environ['KAGGLE_USERNAME'] = "your_kaggle_username"  # Replace with environment variable
    os.environ['KAGGLE_KEY'] = "your_kaggle_key"  # Replace with environment variable
    
def download_kaggle_datasets():
    """Download datasets from Kaggle"""
    try:
        setup_kaggle()
        data_dir = Path("data/external")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        for name, dataset in KAGGLE_DATASETS.items():
            output_dir = data_dir / name
            if not output_dir.exists():
                logger.info(f"Downloading {name} dataset...")
                kaggle.api.dataset_download_files(
                    dataset,
                    path=output_dir,
                    unzip=True
                )
                logger.info(f"Downloaded {name} dataset to {output_dir}")
                
    except Exception as e:
        logger.error(f"Error downloading Kaggle datasets: {str(e)}")
        raise

def download_huggingface_models():
    """Download pre-trained models from Hugging Face"""
    try:
        model_dir = Path("models/pretrained/huggingface")
        model_dir.mkdir(parents=True, exist_ok=True)
        
        for name, model_id in HUGGINGFACE_MODELS.items():
            model_path = model_dir / name
            if not model_path.exists():
                logger.info(f"Downloading {name} model...")
                
                # Download tokenizer and model
                tokenizer = AutoTokenizer.from_pretrained(model_id)
                model = AutoModel.from_pretrained(model_id)
                
                # Save locally
                tokenizer.save_pretrained(model_path)
                model.save_pretrained(model_path)
                
                logger.info(f"Downloaded {name} model to {model_path}")
                
    except Exception as e:
        logger.error(f"Error downloading Hugging Face models: {str(e)}")
        raise

def download_cicids2017():
    """Download CICIDS2017 dataset (alternative source)"""
    try:
        url = "https://www.unb.ca/cic/datasets/ids-2017.html"
        data_dir = Path("data/external/cicids2017")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Note: This is a placeholder. The actual download would need to handle:
        # 1. Authentication on the UNB website
        # 2. Large file downloads (multiple GB)
        # 3. Proper data extraction
        logger.warning("CICIDS2017 download requires manual intervention")
        logger.info(f"Please download the dataset from: {url}")
        logger.info(f"And place the files in: {data_dir}")
        
    except Exception as e:
        logger.error(f"Error downloading CICIDS2017: {str(e)}")
        raise

def prepare_datasets():
    """Prepare downloaded datasets for training"""
    try:
        # Process NSL-KDD dataset
        nsl_kdd_dir = Path("data/external/nsl-kdd")
        if nsl_kdd_dir.exists():
            logger.info("Processing NSL-KDD dataset...")
            # Add processing code here
            
        # Process CICIDS2017 dataset
        cicids_dir = Path("data/external/cicids2017")
        if cicids_dir.exists():
            logger.info("Processing CICIDS2017 dataset...")
            # Add processing code here
            
        # Process system logs dataset
        logs_dir = Path("data/external/system-logs")
        if logs_dir.exists():
            logger.info("Processing system logs dataset...")
            # Add processing code here
            
    except Exception as e:
        logger.error(f"Error preparing datasets: {str(e)}")
        raise

def verify_resources():
    """Verify downloaded resources"""
    try:
        # Check datasets
        for name in KAGGLE_DATASETS.keys():
            path = Path(f"data/external/{name}")
            if not path.exists():
                logger.warning(f"Dataset {name} not found")
            else:
                logger.info(f"Dataset {name} verified")
                
        # Check models
        for name in HUGGINGFACE_MODELS.keys():
            path = Path(f"models/pretrained/huggingface/{name}")
            if not path.exists():
                logger.warning(f"Model {name} not found")
            else:
                logger.info(f"Model {name} verified")
                
    except Exception as e:
        logger.error(f"Error verifying resources: {str(e)}")
        raise

def download_all_resources():
    """Download all external ML resources"""
    logger.info("Starting resource download...")
    
    # Create necessary directories
    Path("data/external").mkdir(parents=True, exist_ok=True)
    Path("models/pretrained/huggingface").mkdir(parents=True, exist_ok=True)
    
    # Download resources
    download_kaggle_datasets()
    download_huggingface_models()
    download_cicids2017()
    
    # Prepare datasets
    prepare_datasets()
    
    # Verify downloads
    verify_resources()
    
    logger.info("Resource download completed!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    download_all_resources() 