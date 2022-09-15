from ovl.utils.types import VisionLike

from crossair.camera_utilities.video_camera import VideoCamera


class PipelineIteration:
    def __init__(self, image):
        self.image = image
        self.processed_image = None
        self.raw_targets = None
        self.targets = None
        self.directions = None


class PipelineTask:
    def __init__(self, pipline: VisionLike, source: VideoCamera):
        self.pipeline: VisionLike = pipline
        self.task = None
        self.iteration = None
        self.source = source

    async def pipeline_task(self):
        while True:
            self.iteration = PipelineIteration(self.source.frame)

            filtered_image = self.pipeline.apply_image_filters(self.iteration.image)
            self.iteration.processed_image = filtered_image

            raw_targets = self.pipeline.detector.detect(filtered_image)
            self.iteration.targets = raw_targets
            targets = self.pipeline.apply_target_filters(raw_targets)
            self.iteration.targets = targets

            self.iteration.directions = self.pipeline.get_directions(targets, self.iteration.image)

    def run_pipeline(self, source: VideoCamera):
        pass
