from typing import Dict

import pydantic

from snowyovl.camera_utilities.typing import CameraSource


class CameraStatus(pydantic.BaseModel):
    camera_source: str
    created_at: str
    status: str


class CamerasStatuses(pydantic.BaseModel):
    cameras: Dict[CameraSource, CameraStatus]
