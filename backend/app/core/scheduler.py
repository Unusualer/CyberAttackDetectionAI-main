from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from ..services.ml.training_pipeline import ModelTrainingPipeline
from ..services.backup import BackupService
from ..services.threat_intelligence import ThreatIntelligence

scheduler = AsyncIOScheduler()

async def setup_scheduled_tasks():
    # Model retraining - every day at 2 AM
    scheduler.add_job(
        ModelTrainingPipeline().retrain_models,
        CronTrigger(hour=2)
    )
    
    # Daily backup - every day at 1 AM
    scheduler.add_job(
        BackupService().create_backup,
        CronTrigger(hour=1)
    )
    
    # Update threat intelligence - every 6 hours
    scheduler.add_job(
        ThreatIntelligence().update_indicators,
        CronTrigger(hour='*/6')
    )
    
    scheduler.start() 