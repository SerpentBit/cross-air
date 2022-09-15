import asyncio
from asyncio import to_thread
from typing import Dict, Union
from uuid import uuid4

import cv2
from fastapi import Depends, HTTPException
from starlette import status
from structlog import get_logger
from structlog.contextvars import bound_contextvars

from crossair.camera_utilities.camera_handler import CameraHandler
from crossair.camera_utilities.typing import CameraSource
from crossair.camera_utilities.video_camera import VideoCamera

logger = get_logger(__name__)

active_camera_handlers: Dict[CameraSource, CameraHandler] = {}


def is_camera_available(source: int):
    camera = cv2.VideoCapture(source)
    source_exists = camera.isOpened()
    camera.release()
    return source_exists


def camera_session_id():
    return uuid4().hex


CAMERA_START_DELAY = 1


async def _provide_camera(source: CameraSource, uuid) -> VideoCamera:
    if source not in active_camera_handlers:
        camera = VideoCamera(source, encode_type=".jpeg")
        camera_handler = CameraHandler(camera)
        active_camera_handlers[source] = camera_handler
        await asyncio.sleep(CAMERA_START_DELAY)
        logger.info(f"Camera {source} started")
    active_camera_handlers[source].add_consumer(uuid)
    logger.info(f"Added consumer {uuid}")
    return active_camera_handlers[source].camera


async def ensure_camera(source: int, uuid: str = Depends(camera_session_id)) -> VideoCamera:
    with bound_threadlocal(source=source, uuid=uuid):
        yield _provide_camera(source, uuid)
        active_camera_handlers[source].remove_consumer(uuid)
        logger.info(f"Consumer disconnected")
        if not active_camera_handlers[source].consumers:
            logger.debug(f"Camera stopped")
            del active_camera_handlers[source]


async def get_camera(source: int) -> Union[VideoCamera, None]:
    with bound_contextvars(source=source):
        if source not in active_camera_handlers:
            return None
        elif not await to_thread(is_camera_available, source):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"The Camera source '{source}' is not available")
        else:
            return active_camera_handlers[source].camera
