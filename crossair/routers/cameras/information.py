import fastapi
from fastapi import Depends

from crossair.dependencies.camera_dependency import get_camera

information = fastapi.APIRouter(dependencies=[Depends(get_camera)], tags=["Information"])


@information.get("")
async def camera_info(camera=Depends(get_camera)):
    if camera:
        return camera.camera_info()
    else:
        return {"status": "inactive"}
