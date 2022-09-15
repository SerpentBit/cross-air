from typing import Dict

import pydantic

from crossair.camera_utilities.typing import CameraSource


class CameraStatus(pydantic.BaseModel):
    camera_source: str
    created_at: str
    status: str
