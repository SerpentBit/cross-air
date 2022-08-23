import asyncio
from typing import Dict, Union
from uuid import uuid4

import cv2
from fastapi import Depends, HTTPException
from starlette import status
from structlog import get_logger

from crossair.camera_utilities.camera_handler import CameraHandler
from crossair.camera_utilities.typing import CameraSource
from crossair.camera_utilities.video_camera import VideoCamera

logger = get_logger(__name__)

cameras: Dict[CameraSource, CameraHandler] = {}


def is_camera_available(source: int):
    camera = cv2.VideoCapture(source)
    source_exists = camera.isOpened()
    camera.release()
    return source_exists


def camera_session_id():
    return uuid4().hex


CAMERA_START_DELAY = 1


async def _get_or_open_camera(source: CameraSource, uuid) -> VideoCamera:
    if source not in cameras:
        camera = VideoCamera(source, encode_type=".jpeg")
        camera_handler = CameraHandler(camera)
        cameras[source] = camera_handler
        await asyncio.sleep(CAMERA_START_DELAY)
        logger.info(f"Camera {source} started")
    cameras[source].add_consumer(uuid)
    logger.info(f"Added consumer {uuid}")
    return cameras[source].camera


async def ensure_camera(source: int, uuid: str = Depends(camera_session_id)) -> VideoCamera:
    yield _get_or_open_camera(source, uuid)
    cameras[source].remove_consumer(uuid)
    logger.info(f"Consumer {uuid} disconnected")
    if not cameras[source].consumers:
        logger.debug(f"Camera {source} stopped")
        del cameras[source]


async def get_camera(source: int) -> Union[VideoCamera, None]:
    if source not in cameras:
        return None
    elif not is_camera_available(source):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The Camera source '{source}' is not available")
    else:
        return cameras[source].camera
