import ovl
from fastapi import HTTPException
from starlette import status

pipelines = {}


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
