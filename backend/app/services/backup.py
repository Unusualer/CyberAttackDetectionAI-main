from typing import Dict, Any, List
import asyncio
from datetime import datetime, timedelta
import boto3
import json
import gzip
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class BackupService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION
        )
        self.backup_bucket = settings.BACKUP_BUCKET
        
    async def create_backup(self) -> Dict[str, Any]:
        """Create a full system backup"""
        try:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            
            # Backup database
            db_backup = await self._backup_database()
            
            # Backup ML models
            model_backup = await self._backup_models()
            
            # Backup configuration
            config_backup = await self._backup_configuration()
            
            # Create backup manifest
            manifest = {
                "timestamp": timestamp,
                "components": {
                    "database": db_backup,
                    "models": model_backup,
                    "configuration": config_backup
                },
                "metadata": {
                    "version": settings.VERSION,
                    "environment": settings.ENVIRONMENT
                }
            }
            
            # Upload manifest
            manifest_key = f"backups/{timestamp}/manifest.json"
            self.s3_client.put_object(
                Bucket=self.backup_bucket,
                Key=manifest_key,
                Body=json.dumps(manifest)
            )
            
            logger.info(f"Backup completed successfully: {timestamp}")
            return manifest
            
        except Exception as e:
            logger.error(f"Backup failed: {str(e)}")
            raise
            
    async def restore_backup(self, backup_id: str) -> Dict[str, Any]:
        """Restore system from backup"""
        try:
            # Get backup manifest
            manifest_key = f"backups/{backup_id}/manifest.json"
            manifest = json.loads(
                self.s3_client.get_object(
                    Bucket=self.backup_bucket,
                    Key=manifest_key
                )["Body"].read()
            )
            
            # Restore components in order
            await self._restore_database(manifest["components"]["database"])
            await self._restore_models(manifest["components"]["models"])
            await self._restore_configuration(manifest["components"]["configuration"])
            
            logger.info(f"Restore completed successfully: {backup_id}")
            return {"status": "success", "backup_id": backup_id}
            
        except Exception as e:
            logger.error(f"Restore failed: {str(e)}")
            raise
            
    async def _backup_database(self) -> Dict[str, Any]:
        """Backup PostgreSQL database"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_file = f"db_backup_{timestamp}.sql.gz"
        
        try:
            # Create database dump
            process = await asyncio.create_subprocess_shell(
                f"pg_dump {settings.DATABASE_URL} | gzip > {backup_file}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            
            # Upload to S3
            backup_key = f"backups/{timestamp}/database/{backup_file}"
            with open(backup_file, 'rb') as f:
                self.s3_client.upload_fileobj(f, self.backup_bucket, backup_key)
                
            return {
                "file": backup_key,
                "timestamp": timestamp,
                "size": await self._get_file_size(backup_file)
            }
            
        finally:
            # Cleanup
            await asyncio.create_subprocess_shell(f"rm {backup_file}")
            
    async def _backup_models(self) -> Dict[str, Any]:
        """Backup ML models"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        models_dir = settings.MODEL_PATH
        backup_file = f"models_backup_{timestamp}.tar.gz"
        
        try:
            # Create models archive
            process = await asyncio.create_subprocess_shell(
                f"tar -czf {backup_file} -C {models_dir} .",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            
            # Upload to S3
            backup_key = f"backups/{timestamp}/models/{backup_file}"
            with open(backup_file, 'rb') as f:
                self.s3_client.upload_fileobj(f, self.backup_bucket, backup_key)
                
            return {
                "file": backup_key,
                "timestamp": timestamp,
                "size": await self._get_file_size(backup_file)
            }
            
        finally:
            # Cleanup
            await asyncio.create_subprocess_shell(f"rm {backup_file}")
            
    async def _restore_database(self, backup_info: Dict[str, Any]) -> None:
        """Restore database from backup"""
        backup_file = "db_restore.sql.gz"
        
        try:
            # Download backup
            self.s3_client.download_file(
                self.backup_bucket,
                backup_info["file"],
                backup_file
            )
            
            # Restore database
            process = await asyncio.create_subprocess_shell(
                f"gunzip -c {backup_file} | psql {settings.DATABASE_URL}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            
        finally:
            # Cleanup
            await asyncio.create_subprocess_shell(f"rm {backup_file}") 