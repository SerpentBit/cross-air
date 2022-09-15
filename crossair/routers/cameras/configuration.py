from fastapi import APIRouter, Depends

from crossair.camera_utilities.camera_handler import CameraHandler
from crossair.camera_utilities.response_models import CameraConfigurationResponse
from crossair.camera_utilities.typing import CameraConfiguration, CameraSource
from crossair.camera_utilities.exceptions import CameraConfigurationError
from crossair.dependencies.camera_dependency import ensure_camera

camera_configuration = APIRouter()


@camera_configuration.get("/cameras/{source}/configuration")
async def get_camera_configuration(camera: CameraHandler = Depends(ensure_camera)):
    return camera.camera.camera_info()


@camera_configuration.put("/cameras/{source}/configuration", response_model=CameraConfigurationResponse)
async def change_camera_configuration(source: CameraSource, configuration: CameraConfiguration,
                                      camera: CameraHandler = Depends(ensure_camera)):
    try:
        # TODO: Implement camera configuration failure handling
        return CameraConfigurationResponse(message=f"Successfully configured camera {source}", )
    except CameraConfigurationError as error:
        return f"Failed to configure camera {source}"
