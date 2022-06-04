class CameraConfigurationError(Exception):
    def __init__(self, configured_properties, failed_properties, left_over_properties):
        self.configured_properties = configured_properties
        self.failed_properties = failed_properties
        self.left_over_properties = left_over_properties
