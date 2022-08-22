from .camera.configuration import camera_configuration
from .camera.information import information
from .camera.stream import stream

routers = (camera_configuration, stream, information)
