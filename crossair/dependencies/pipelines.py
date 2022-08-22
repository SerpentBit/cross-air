import copy
from typing import Any

import ovl
import pydantic
from fastapi import HTTPException
from starlette import status

target_filters = [ovl.percent_area_filter(minimal_percent=2), ovl.area_sort()]

red_circle = ovl.Vision(target_filters=target_filters, threshold=ovl.HSV.red)
green_circle = copy.copy(red_circle)
green_circle.detector = ovl.ThresholdDetector(threshold=ovl.HSV.green)

yellow_circle = copy.copy(red_circle)
yellow_circle.detector = ovl.ThresholdDetector(threshold=ovl.HSV.yellow)

pipelines = {"Red": red_circle, "Green": green_circle, "Yellow": yellow_circle}


async def provide_pipeline(pipeline_id) -> ovl.Vision:
    if pipeline_id not in pipelines:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pipeline {pipeline_id} not found")
    return pipelines[pipeline_id]


async def add_pipeline(pipeline_id, pipeline):
    if pipeline_id in pipeline:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Pipeline {pipeline_id} already exists")
    pipelines[pipeline_id] = pipeline
    return pipeline_id, pipeline


class PipelineDeltaBase(pydantic.BaseModel):
    pass


class SerializedVision(pydantic.BaseModel):
    pass


async def extract_pipeline(pipeline_package: SerializedVision | PipelineDeltaBase):
    raise NotImplementedError()
