import typing

from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse
from starlette.types import Send
from starlette import status

from crossair.cameras.stream.dependencies import IMAGE_STREAM_MEDIA_TYPE


class ImageStream(StreamingResponse):
    def __init__(self,
                 content: typing.Any,
                 status_code: int = status.HTTP_200_OK,
                 headers: dict = None,
                 media_type: str = None,
                 background: BackgroundTask = None) -> None:
        super().__init__(content, status_code, headers, media_type=media_type or IMAGE_STREAM_MEDIA_TYPE,
                         background=background)

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
