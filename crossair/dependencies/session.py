import enum
from functools import lru_cache

from fastapi import Depends
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.types import Send

from crossair.camera_utilities.video_camera import VideoCamera
from crossair.dependencies.camera_dependency import ensure_camera

IMAGE_CONTENT_CACHE_SIZE = 32


@lru_cache(maxsize=IMAGE_CONTENT_CACHE_SIZE)
def prepare_image(encoded_image):
    return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n'


class ImageStream(StreamingResponse):

    async def stream_response(self, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )
        async for chunk in self.body_iterator:
            if not isinstance(chunk, bytes):
                chunk = chunk.encode(self.charset)
            await send({"type": "http.response.body", "body": chunk, "more_body": True})
        await send({"type": "http.response.body", "body": b"", "more_body": False})


class ConnectionStatus(enum.Enum):
    client_disconnect = False
    camera_disconnect = False
    connected = True

    @property
    def is_connected(self):
        return self.value


async def is_stream_connected(request: Request, camera: VideoCamera) -> ConnectionStatus:
    if await request.is_disconnected():
        return ConnectionStatus.client_disconnect
    elif not camera.active:
        return ConnectionStatus.camera_disconnect
    return ConnectionStatus.connected


def provide_session_handler(request: Request, camera: VideoCamera = Depends(ensure_camera)):
    async def session_handler(image_source, on_finish: callable):
        async def generate():
            while connection_status := is_stream_connected(request, camera):
                if (image := await anext(image_source)) is not None:
                    yield prepare_image(image)
            on_finish(connection_status)

        return generate()

    return session_handler
