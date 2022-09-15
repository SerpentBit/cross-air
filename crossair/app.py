import fastapi
import structlog
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from crossair.cameras.base_router import cameras_router

logger = structlog.get_logger(__name__)

app = fastapi.FastAPI()

ORIGINS = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROUTERS = (cameras_router, pipelines_router)
for router in ROUTERS:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000,)
