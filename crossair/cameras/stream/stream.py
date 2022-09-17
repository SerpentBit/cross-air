from fastapi import Depends, APIRouter
from starlette.responses import StreamingResponse
from structlog import get_logger

from crossair.cameras.dependencies import camera_session_id, ensure_camera
from crossair.cameras.stream.dependencies import provide_session_handler
from crossair.cameras.responses import ImageStream

logger = get_logger(__name__)

streams_router = APIRouter(prefix="/streams", tags=["Streams"])


@streams_router.get("/raw", response_class=StreamingResponse)
async def video_feed(source, camera=Depends(ensure_camera), session=Depends(provide_session_handler),
                     uuid: str = Depends(camera_session_id)):
    logger.info(f"New consumer {uuid} for raw feed {source}")
    return ImageStream(session(camera))


@streams_router.get("/filtered", response_class=StreamingResponse)
async def video_feed(source, camera=Depends(ensure_camera), session=Depends(provide_session_handler),
                     uuid: str = Depends(camera_session_id)):
    logger.info(f"New consumer {uuid} for filtered feed {source}")
    return ImageStream(session(camera))
