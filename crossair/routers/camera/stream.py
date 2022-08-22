from fastapi import Depends, APIRouter
from starlette.responses import StreamingResponse
from structlog import get_logger

from crossair.dependencies.camera_dependency import camera_session_id, ensure_camera
from crossair.dependencies.session import provide_session_handler

stream = APIRouter(prefix="/cameras/{source}/feeds")

logger = get_logger(__name__)

IMAGE_STREAM_MEDIA_TYPE = "multipart/x-mixed-replace;boundary=frame"


async def provide_raw_camera_feed(camera=Depends(ensure_camera)):
    async def raw_camera_feed():
        while True:
            yield camera

    return raw_camera_feed


@stream.get("/raw", response_class=StreamingResponse)
async def video_feed(source, camera_feed=Depends(provide_raw_camera_feed), session=Depends(provide_session_handler),
                     uuid: str = Depends(camera_session_id)):
    logger.info(f"New consumer {uuid} for raw feed {source}")
    feed = session(camera_feed)
    return StreamingResponse(feed, media_type=IMAGE_STREAM_MEDIA_TYPE)


@stream.get("filtered", response_class=StreamingResponse)
async def video_feed(source, feed=Depends(provide_raw_camera_feed), uuid: str = Depends(camera_session_id),
                     session=Depends(provide_session_handler)):
    logger.info(f"New consumer {uuid} for filtered feed {source}")
    return StreamingResponse(session(feed()), media_type=IMAGE_STREAM_MEDIA_TYPE)
