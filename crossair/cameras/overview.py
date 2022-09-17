from fastapi import APIRouter

from crossair.cameras.dependencies import camera_handlers

overview_router = APIRouter(prefix="/overview")


