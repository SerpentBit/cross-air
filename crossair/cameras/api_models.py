import pydantic


class CameraStatus(pydantic.BaseModel):
    camera_source: str
    created_at: str
    status: str
