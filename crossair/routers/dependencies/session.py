from fastapi import Depends
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.types import Send

from snowyovl.app import prepare_image
from snowyovl.routers.dependencies.camera_dependency import ensure_camera


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


def provide_session_handler(request: Request, camera=Depends(ensure_camera)):
    async def session_handler(image_source, on_finish: callable):
        async def generate():
            while not await request.is_disconnected() or not camera.active:
                image = await image_source.__anext__()
                if image is not None:
                    yield prepare_image(image)
            on_finish()
        return generate()
    return session_handler
