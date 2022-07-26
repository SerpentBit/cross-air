import enum

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from crossair.routers.dependencies.pipelines import provide_pipeline

pipelines_router = APIRouter(prefix="/pipelines")

pipelines_specific = APIRouter(prefix="/{pipeline_id}")


# TODO: Implement pipeline creation
@pipelines_specific.post("/create")
async def create_pipeline(pipeline_id: str, pipeline: str):
    pass


# TODO: Implement pipeline importing

@pipelines_specific.get("")
async def get_pipeline(pipeline=Depends(provide_pipeline)):
    return repr(pipeline)


# TODO: Implement pipeline editing
@pipelines_specific.put("")
async def put_pipeline(pipeline=Depends(provide_pipeline)):
    pass


# TODO: Implement pipeline deletion
@pipelines_specific.delete("")
async def delete_pipeline(pipeline=Depends(provide_pipeline)):
    pass


# TODO: Implement pipeline test on 1 image (Upload image get result)

class PipelineStage(enum.Enum):
    processing = "processing"
    detection = "detection"
    filtering = "filtering"
    direction = "direction"


class PipelineApplication(BaseModel):
    stage: PipelineStage


@pipelines_specific.post("/apply")
async def test_pipeline(pipeline=Depends(provide_pipeline), application=PipelineApplication):
    pass


pipelines_router.include_router(pipelines_specific)
