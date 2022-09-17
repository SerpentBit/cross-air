from fastapi import APIRouter

from crossair.cameras.dependencies import camera_handlers
from crossair.cameras.overview import overview_router
from crossair.cameras.configuration import camera_configuration_router
from crossair.cameras.stream.stream import streams_router

cameras_router = APIRouter(prefix="/cameras")

# region specific_camera
specific_camera_router = APIRouter(prefix="/{camera_source}")
sub_routers = (camera_configuration_router, streams_router)

for router in sub_routers:
    specific_camera_router.include_router(router)
# endregion


@cameras_router.get("/overview", tags=["Overview"])
async def get_all_cameras_info():
    return {
        source: camera.camera.camera_info()
        for source, camera in camera_handlers.items()
    }

cameras_router.include_router(specific_camera_router)
cameras_router.include_router(overview_router)
