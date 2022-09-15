from fastapi import Depends, APIRouter
from starlette.responses import StreamingResponse
from structlog import get_logger

from crossair.dependencies.camera_dependency import camera_session_id, ensure_camera, active_camera_handlers, get_camera
from crossair.dependencies.session import provide_session_handler
from crossair.routers.cameras.responses import ImageStream

stream = APIRouter(prefix="/cameras/{source}/feeds", tags=["Streams"])

logger = get_logger(__name__)


@stream.get("/raw", response_class=StreamingResponse)
async def video_feed(source, camera=Depends(ensure_camera), session=Depends(provide_session_handler),
                     uuid: str = Depends(camera_session_id)):
    logger.info(f"New consumer {uuid} for raw feed {source}")
    return ImageStream(session(camera))


@stream.get("filtered", response_class=StreamingResponse)
async def video_feed(source, camera=Depends(ensure_camera), uuid: str = Depends(camera_session_id),
                     session=Depends(provide_session_handler)):
    logger.info(f"New consumer {uuid} for filtered feed {source}")
    return ImageStream(session(camera))


@stream.delete("/cameras/{source}", dependencies=[Depends(get_camera)])
async def close_camera(source: int):
    active_camera_handlers[source].camera.stop()
    del active_camera_handlers[source]
