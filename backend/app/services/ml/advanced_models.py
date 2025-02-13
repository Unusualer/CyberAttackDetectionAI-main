import tensorflow as tf
from transformers import TFBertForSequenceClassification, BertTokenizer, AutoTokenizer
from .base import BaseMLModel
import numpy as np
from ...core.config import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TransformerThreatDetector(BaseMLModel):
    def __init__(self):
        super().__init__()
        self.model = TFBertForSequenceClassification.from_pretrained(
            'distilbert-base-uncased',
            num_labels=len(self.threat_types)
        )
        self.tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
        self.max_length = settings.MAX_SEQUENCE_LENGTH
        self.batch_size = 32
        
    async def detect_complex_patterns(self, sequence_data: List[str]) -> Dict[str, Any]:
        """Detect complex attack patterns using transformers"""
        try:
            results = []
            for i in range(0, len(sequence_data), self.batch_size):
                batch = sequence_data[i:i + self.batch_size]
                inputs = self.tokenizer(
                    batch,
                    padding=True,
                    truncation=True,
                    max_length=self.max_length,
                    return_tensors="tf"
                )
                
                with tf.keras.mixed_precision.experimental.policy('mixed_float16'):
                    outputs = self.model(inputs)
                predictions = tf.nn.softmax(outputs.logits, axis=-1)
                
                for pred in predictions:
                    threat_type = self.threat_types[tf.argmax(pred)]
                    confidence = float(tf.reduce_max(pred))
                    results.append({
                        "threat_type": threat_type,
                        "confidence": confidence,
                        "probabilities": {
                            t_type: float(prob)
                            for t_type, prob in zip(self.threat_types, pred.numpy())
                        }
                    })
                    
            return {
                "predictions": results,
                "model_version": self.model.config.version,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in transformer threat detection: {str(e)}")
            raise
            
    async def train(
        self,
        train_texts: List[str],
        train_labels: List[int],
        validation_data: tuple = None,
        **kwargs
    ):
        """Train the transformer model"""
        try:
            # Prepare training data
            train_encodings = self.tokenizer(
                train_texts,
                truncation=True,
                padding=True,
                max_length=self.max_length,
                return_tensors="tf"
            )
            
            # Convert labels to tensor
            train_labels = tf.convert_to_tensor(train_labels)
            
            # Compile model
            self.model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5),
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy']
            )
            
            # Train model
            history = self.model.fit(
                train_encodings,
                train_labels,
                validation_data=validation_data,
                epochs=kwargs.get('epochs', 3),
                batch_size=kwargs.get('batch_size', 16)
            )
            
            return history
            
        except Exception as e:
            logger.error(f"Error training transformer model: {str(e)}")
            raise