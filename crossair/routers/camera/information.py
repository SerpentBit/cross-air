import fastapi
from fastapi import Depends

from snowyovl.routers.camera.api_models import CamerasStatuses
from snowyovl.routers.dependencies.camera_dependency import get_camera, cameras

information = fastapi.APIRouter(dependencies=[Depends(get_camera)])


@information.get("/cameras/{source}")
async def camera_info(camera=Depends(get_camera)):
    if camera:
        return camera.camera_info()
    else:
        return {"status": "inactive"}


@information.get("/cameras/{source}/status")
async def camera_status(camera=Depends(get_camera)):
    return {"status": "active" if camera else "inactive"}


@information.delete("/camera/{source}", dependencies=[Depends(get_camera)])
async def close_camera(source: int):
    cameras[source].camera.stop()
    del cameras[source]


@information.get("/cameras/status", response_model=CamerasStatuses)
async def get_all_cameras_status():
    return {
        source: camera.camera.active
        for source, camera in cameras.items()
    }


@information.get("/cameras/info")
async def get_all_cameras_info():
    return {
        source: camera.camera.camera_info()
        for source, camera in cameras.items()
    }
