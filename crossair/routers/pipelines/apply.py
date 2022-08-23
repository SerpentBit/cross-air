import enum

import fastapi
from fastapi import Depends, UploadFile
from pydantic import BaseModel

from crossair.dependencies.pipelines import provide_pipeline

apply = fastapi.APIRouter()


class PipelineStage(enum.Enum):
    processing = "apply_image_filters"
    detection = "detect"
    filtering = "apply_image_filters"
    direction = "get_directions"


def stage_functions(pipeline, stage):
    for current_stage in PipelineStage:
        if current_stage.name != stage:
            yield current_stage.name, getattr(pipeline, stage.name)
        return stage.name, getattr(pipeline, stage.name)


class PipelineApplication(BaseModel):
    stage: PipelineStage


@apply.post("/apply")
async def test_pipeline(image=UploadFile, pipeline=Depends(provide_pipeline), application=PipelineApplication):
    stage_result = image
    for stage_name, stage_function in stage_functions(application.stage, pipeline):
        result = stage_function(stage_result)
    return stage_result
