from snowyovl.camera_utilities.video_camera import VideoCamera
from snowyovl.pipeline_utilities.pipeline import Pipeline


class PipelineIteration:
    def __init__(self, image):
        self.image = image
        self.processed_image = None
        self.raw_targets = None
        self.targets = None
        self.directions = None


class PipelineTask:
    def __init__(self, pipline: Pipeline, source: VideoCamera):
        self.pipeline = pipline
        self.task = None
        self.iteration = None
        self.source = source

    async def pipeline_task(self):
        while True:
            image = await self.source.frame()
            self.iteration = PipelineIteration(image)

            filtered_image = self.pipeline.pipeline.apply_image_filters(image)
            self.iteration.processed_image = filtered_image

            raw_targets = self.pipeline.pipeline.detector.detect(filtered_image)
            self.iteration.targets = raw_targets
            targets = self.pipeline.pipeline.apply_target_filters(raw_targets)
            self.iteration.targets = targets

            self.iteration.directions = self.pipeline.pipeline.get_directions(targets, image)

    def run_pipeline(self, source: VideoCamera):
