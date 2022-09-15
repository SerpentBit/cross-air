import enum
from functools import lru_cache

from starlette.requests import Request

from crossair.camera_utilities.video_camera import VideoCamera

IMAGE_CONTENT_CACHE_SIZE = 32
IMAGE_HEADER = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
IMAGE_ESCAPE = b'\r\n'
IMAGE_STREAM_MEDIA_TYPE = "multipart/x-mixed-replace;boundary=frame"


@lru_cache(maxsize=IMAGE_CONTENT_CACHE_SIZE)
def prepare_image(encoded_image):
    return IMAGE_HEADER + bytearray(encoded_image) + IMAGE_ESCAPE


class ConnectionStatus(enum.Enum):
    client_disconnect = False
    camera_disconnect = False
    connected = True

    @property
    def is_connected(self):
        return self.value


async def is_stream_connected(request: Request, camera: VideoCamera) -> ConnectionStatus:
    if not camera.active:
        return ConnectionStatus.camera_disconnect
    elif await request.is_disconnected():
        return ConnectionStatus.client_disconnect
    return ConnectionStatus.connected


def provide_session_handler(request: Request):
    async def session_handler(camera, on_finish: callable):
        async def generate():
            while connection_status := is_stream_connected(request, camera):
                if (image := await anext(camera)) is not None:
                    yield prepare_image(image)
            on_finish(connection_status)

        return generate()

    return session_handler
