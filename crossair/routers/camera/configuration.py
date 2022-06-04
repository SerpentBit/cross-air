from fastapi import APIRouter, Depends

from crossair.camera_utilities.camera_handler import CameraHandler
from crossair.camera_utilities.response_models import CameraConfigurationResponse
from crossair.camera_utilities.typing import CameraConfiguration, CameraSource
from crossair.camera_utilities.exceptions import CameraConfigurationError
from crossair.routers.dependencies.camera_dependency import ensure_camera

camera_configuration = APIRouter()


@camera_configuration.get("/camera/{source}/configuration")
async def get_camera_configuration(camera: CameraHandler = Depends(ensure_camera)):
    return camera.camera.camera_info()


@camera_configuration.put("/camera/{source}/configuration", response_model=CameraConfigurationResponse)
async def change_camera_configuration(source: CameraSource, configuration: CameraConfiguration,
                                      camera: CameraHandler = Depends(ensure_camera)):
    try:
        # TODO: Implement camera configuration failure handling
        return CameraConfigurationResponse(message=f"Successfully configured camera {source}", )
    except CameraConfigurationError as e:
        return f"Failed to configure camera {source}"
