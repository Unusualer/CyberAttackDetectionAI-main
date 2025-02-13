from typing import Dict, Set
from fastapi import WebSocket
import logging
import json
import asyncio

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        
    async def connect(self, websocket: WebSocket, organization_id: str):
        await websocket.accept()
        if organization_id not in self.active_connections:
            self.active_connections[organization_id] = set()
        self.active_connections[organization_id].add(websocket)
        logger.info(f"New WebSocket connection for organization {organization_id}")
        
    def disconnect(self, websocket: WebSocket, organization_id: str):
        self.active_connections[organization_id].remove(websocket)
        if not self.active_connections[organization_id]:
            del self.active_connections[organization_id]
        logger.info(f"WebSocket disconnected for organization {organization_id}")
        
    async def broadcast_to_organization(self, organization_id: str, message: dict):
        if organization_id not in self.active_connections:
            return
            
        disconnected = set()
        for connection in self.active_connections[organization_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error sending message: {str(e)}")
                disconnected.add(connection)
                
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection, organization_id)

websocket_manager = WebSocketManager() 