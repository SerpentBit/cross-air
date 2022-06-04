from typing import List, Optional

from pydantic import BaseModel

from snowyovl.camera_utils.typing import CameraParameters


class CameraConfigurationResponse(BaseModel):
    message: str
    configured_properties: List[CameraParameters]
    failed_properties: List[CameraParameters]
    error: Optional[str]
