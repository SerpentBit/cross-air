from asyncio import to_thread

from crossair.camera_utilities.video_camera import VideoCamera


class CameraHandler:
    def __init__(self, camera: VideoCamera):
        self.camera = camera
        self.consumers = []

    def add_consumer(self, consumer_id):
        self.consumers.append(consumer_id)

    async def camera_info(self):
        return await to_thread(self.camera.camera_info)

    def remove_consumer(self, consumer_id):
        self.consumers.remove(consumer_id)
        if not self.consumers:
            self.camera.stop()
