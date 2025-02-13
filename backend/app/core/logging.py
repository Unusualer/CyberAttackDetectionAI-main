import logging
import logging.config
from datetime import datetime
import json
import traceback
from typing import Dict, Any
from pythonjsonlogger import jsonlogger
from ..core.config import settings

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]) -> None:
        super().add_fields(log_record, record, message_dict)
        
        # Add custom fields
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['environment'] = settings.ENVIRONMENT
        
        # Add error details if present
        if record.exc_info:
            log_record['error_type'] = record.exc_info[0].__name__
            log_record['error_message'] = str(record.exc_info[1])
            log_record['stacktrace'] = traceback.format_exception(*record.exc_info)

def setup_logging():
    """Configure application logging"""
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": CustomJsonFormatter,
                "format": "%(timestamp)s %(level)s %(name)s %(message)s"
            },
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": f"logs/{settings.ENVIRONMENT}/app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": f"logs/{settings.ENVIRONMENT}/error.log",
                "maxBytes": 10485760,
                "backupCount": 5,
                "level": "ERROR"
            },
            "security": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": f"logs/{settings.ENVIRONMENT}/security.log",
                "maxBytes": 10485760,
                "backupCount": 10
            }
        },
        "loggers": {
            "app": {
                "handlers": ["console", "file"],
                "level": settings.LOG_LEVEL,
                "propagate": False
            },
            "app.security": {
                "handlers": ["security", "console"],
                "level": "INFO",
                "propagate": False
            },
            "app.ml": {
                "handlers": ["file", "console"],
                "level": "INFO",
                "propagate": False
            },
            "app.api": {
                "handlers": ["file", "console"],
                "level": "INFO",
                "propagate": False
            }
        },
        "root": {
            "handlers": ["console", "error_file"],
            "level": "WARNING"
        }
    }
    
    logging.config.dictConfig(config) 