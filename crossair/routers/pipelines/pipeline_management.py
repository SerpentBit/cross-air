from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from crossair.dependencies.pipelines import extract_pipeline
from crossair.pipeline_utilities.pipeline import Pipeline

pipeline_management = APIRouter()


@pipeline_management.post("/create")
async def create_pipeline(pipeline_id: str, pipeline: Pipeline = Depends(extract_pipeline)):
    raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="Creating Pipelines isn't implement yet")


# TODO: Define loadout functionality in the general sense
@pipeline_management.get("/loadout")
async def get_current_load_out():
    raise HTTPException(detail="Loadouts arent implemented yet", status_code=status.HTTP_423_LOCKED)
