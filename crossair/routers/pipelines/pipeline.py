from fastapi import APIRouter

pipelines = APIRouter(prefix="/pipelines/{pipeline_id}")


@pipelines.get("")
async def get_pipeline(pipeline_id: str):
    return
