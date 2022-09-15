import fastapi
from fastapi import APIRouter, Depends

from crossair.camera_utilities.camera_handler import CameraHandler
from crossair.camera_utilities.response_models import CameraConfigurationResponse
from crossair.camera_utilities.typing import CameraConfiguration, CameraSource
from crossair.camera_utilities.exceptions import CameraConfigurationError
from crossair.cameras.dependencies import get_camera

camera_configuration_router = APIRouter(prefix="/configuration", tags=["Camera Configuration"])


@camera_configuration_router.get("")
async def camera_info(camera=Depends(get_camera)):
    if camera:
        return camera.camera_info()
    else:
        return fastapi.Response({"status": "inactive"}, status_code=fastapi.status.HTTP_404_NOT_FOUND)


@camera_configuration_router.put("", response_model=CameraConfigurationResponse)
async def change_camera_configuration(source: CameraSource, configuration: CameraConfiguration,
                                      camera: CameraHandler = Depends(get_camera)):
    try:
        # TODO: Implement Camera configuration
        return CameraConfigurationResponse(message=f"Successfully configured camera {source}", )
    except CameraConfigurationError as error:
        # TODO: Implement camera configuration failure handling
        return f"Failed to configure camera {source}"
