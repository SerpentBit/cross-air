import enum
from typing import Union

from ovl import CameraProperties
from pydantic import constr, conint, BaseModel

CameraDeviceSource = constr(regex=r"^(/dev/video[0-9]+)$")
CameraIpSource = constr(regex=r"^(http://[0-9a-zA-Z\.]+:[0-9]+)$")
CameraIpSourceWithAuth = constr(regex=r"^(http://[0-9a-zA-Z\.]+:[0-9]+@[0-9a-zA-Z\.]+:[0-9]+)$")
CameraIdSource = conint(ge=0, le=9)

CameraSource = Union[CameraDeviceSource, CameraIpSource, CameraIpSourceWithAuth, CameraIdSource]
"""
Camera source can be either a path to a device a camera index or a hostname/ip of an ip camera.
"""


class CameraParameters(enum.Enum):
    width = CameraProperties.IMAGE_WIDTH
    height = CameraProperties.IMAGE_HEIGHT
    fps = CameraProperties.CAMERA_FPS
    brightness = CameraProperties.BRIGHTNESS
    contrast = CameraProperties.CONTRAST
    saturation = CameraProperties.SATURATION
    sharpness = CameraProperties.SHARPNESS
    exposure = CameraProperties.EXPOSURE


class CameraConfiguration(BaseModel):
    width: int = 320
    height: int = 240
    fps: int = 30
    brightness: int = None
    contrast: int = None
    saturation: int = None
    sharpness: int = None
    exposure: int = None


def create_configuration(configuration: CameraConfiguration) -> dict:
    configuration = configuration.dict()
    return {getattr(CameraParameters, camera_property): value for camera_property, value in configuration.items()}
