from fastapi import APIRouter

from crossair.routers.cameras.api_models import CamerasStatuses

statuses = APIRouter()


@statuses.get("/cameras/status", response_model=CamerasStatuses)
async def get_all_cameras_status():
    return {
        source: camera.camera.active
        for source, camera in cameras.items()
    }


@statuses.get("/cameras/info")
async def get_all_cameras_info():
    return {
        source: camera.camera.camera_info()
        for source, camera in cameras.items()
    }
