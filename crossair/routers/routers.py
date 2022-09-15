from .cameras.configuration import camera_configuration
from .cameras.information import information
from .cameras.stream import stream

routers = (camera_configuration, stream, information)
