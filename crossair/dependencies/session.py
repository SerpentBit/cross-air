import dataclasses
import enum
from functools import lru_cache

from fastapi import Depends
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.types import Send

from crossair.routers.dependencies.camera_dependency import ensure_camera


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


async def is_stream_connected(request: Request) -> True | Disconnection:
    stream_disconnect = await request.is_disconnected()
    return


def provide_session_handler(request: Request, camera=Depends(ensure_camera)):
    async def session_handler(image_source, on_finish: callable):
        async def generate():
            while ((stream_dc := not await request.is_disconnected())
                   or (camera_dc := not camera.active)):
                if image := await anext(image_source) is not None:
                    yield prepare_image(image)
            on_finish()

        return generate()

    return session_handler


IMAGE_CONTENT_CACHE_SIZE = 32


@lru_cache(maxsize=IMAGE_CONTENT_CACHE_SIZE)
def prepare_image(encoded_image):
    return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n'
