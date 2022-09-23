import asyncio

import cv2
import structlog as structlog

from crossair.camera_utilities.typing import CameraParameters


class EncodeError(Exception):
    pass


logger = structlog.get_logger(__name__)


class VideoCamera:
    def __init__(self, source, encode_type):
        self.camera = cv2.VideoCapture(source)
        self.source = source
        self.frame = None
        self.encode_type = encode_type
        self.encoded_frame = None
        self.camera_thread = asyncio.create_task(self.image_thread(), name=f"camera-thread-{source}")
        self.active = True

    def read_and_encode(self):
        success, image = self.camera.read()
        encoded_image = self.encode_frame(image)
        return encoded_image

    async def image_thread(self):
        try:
            while True:
                self.encoded_frame = await asyncio.to_thread(self.read_and_encode)
        except asyncio.CancelledError:
            logger.debug(f"Camera thread for camera {self.source} cancelled")

    async def __anext__(self):
        yield self.encoded_frame

    def encode_frame(self, image):
        success, encoded_image = cv2.imencode(self.encode_type, image)
        if not success:
            raise EncodeError("Failed to encode image")
        return encoded_image.tobytes()

    def stop(self):
        self.camera_thread.cancel()
        self.camera.release()
        self.active = False

    def camera_info(self):
        properties = {keyword: self.camera.get(keyword) for keyword in CameraParameters.__members__.keys()}
        return {
            "source": self.source,
            "encode_type": self.encode_type,
            "status": "active",
            **properties
        }
