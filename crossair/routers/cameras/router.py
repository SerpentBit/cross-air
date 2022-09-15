from fastapi import APIRouter

camera_feed = APIRouter(prefix="/cameras/{camera_source}")