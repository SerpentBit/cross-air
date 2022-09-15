from fastapi import APIRouter, Depends

from crossair.pipelines.dependencies import provide_pipeline

pipeline_router = APIRouter(prefix="/{pipeline_id}")


# TODO: Implement pipeline importing

@pipeline_router.get("")
async def get_pipeline(pipeline=Depends(provide_pipeline)):
    return repr(pipeline)


# TODO: Implement pipeline editing
@pipeline_router.put("")
async def put_pipeline(pipeline=Depends(provide_pipeline)):
    pass


# TODO: Implement pipeline deletion
@pipeline_router.delete("")
async def delete_pipeline(pipeline=Depends(provide_pipeline)):
    pass
