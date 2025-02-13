#!/usr/bin/env python3
import asyncio
import argparse
import sys
from app.services.backup import BackupService
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def perform_recovery(backup_id: str, components: List[str] = None):
    """Perform system recovery"""
    try:
        backup_service = BackupService()
        
        # Verify backup exists
        try:
            manifest = await backup_service.get_backup_manifest(backup_id)
        except Exception as e:
            logger.error(f"Backup {backup_id} not found: {str(e)}")
            sys.exit(1)
            
        # Stop services
        logger.info("Stopping services...")
        await stop_services()
        
        # Perform recovery
        logger.info(f"Starting recovery from backup {backup_id}")
        result = await backup_service.restore_backup(
            backup_id,
            components=components
        )
        
        # Verify recovery
        if await verify_recovery(result):
            logger.info("Recovery completed successfully")
            
            # Restart services
            logger.info("Restarting services...")
            await start_services()
        else:
            logger.error("Recovery verification failed")
            await rollback_recovery(backup_id)
            
    except Exception as e:
        logger.error(f"Recovery failed: {str(e)}")
        sys.exit(1)

async def stop_services():
    """Stop all system services"""
    services = [
        "cyber-defense-backend",
        "cyber-defense-ml-engine",
        "nginx"
    ]
    
    for service in services:
        process = await asyncio.create_subprocess_shell(
            f"docker-compose stop {service}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()

async def start_services():
    """Start all system services"""
    process = await asyncio.create_subprocess_shell(
        "docker-compose up -d",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await process.communicate()

async def verify_recovery(result: Dict[str, Any]) -> bool:
    """Verify system recovery"""
    try:
        # Check database
        if not await verify_database():
            return False
            
        # Check ML models
        if not await verify_models():
            return False
            
        # Check system health
        if not await verify_system_health():
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Recovery verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Disaster Recovery Tool")
    parser.add_argument("backup_id", help="Backup ID to restore from")
    parser.add_argument(
        "--components",
        nargs="+",
        help="Specific components to restore (database, models, config)"
    )
    
    args = parser.parse_args()
    asyncio.run(perform_recovery(args.backup_id, args.components)) 