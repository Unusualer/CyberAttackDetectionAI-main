from fastapi import APIRouter, WebSocket, Depends
from ....core.security import get_current_user_ws
from ....services.monitoring import MonitoringService

router = APIRouter()

@router.websocket("/ws/alerts")
async def alerts_websocket(
    websocket: WebSocket,
    current_user = Depends(get_current_user_ws)
):
    await websocket.accept()
    monitoring = MonitoringService()
    
    try:
        async for alert in monitoring.subscribe_to_alerts(
            current_user.organization_id
        ):
            await websocket.send_json(alert)
    except Exception as e:
        await websocket.close(code=1000) 