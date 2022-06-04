from typing import List, Optional

from pydantic import BaseModel

from crossair.camera_utilities.typing import CameraParameters


class CameraConfigurationResponse(BaseModel):
    message: str
    configured_properties: List[CameraParameters]
    failed_properties: List[CameraParameters]
    error: Optional[str]
