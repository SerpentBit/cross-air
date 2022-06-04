from functools import lru_cache

import fastapi
import structlog
import uvicorn
from starlette.middleware.cors import CORSMiddleware

logger = structlog.get_logger(__name__)

app = fastapi.FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMAGE_CONTENT_CACHE_SIZE = 32


@lru_cache(maxsize=IMAGE_CONTENT_CACHE_SIZE)
def prepare_image(encoded_image):
    return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n'


CAMERA_START_DELAY = 1

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000,)
