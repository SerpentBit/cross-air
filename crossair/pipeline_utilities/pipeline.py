from typing import Any, List

import cv2
import numpy
from ovl import Vision, AmbientVision

DEFAULT_TARGET_COLOR = (0, 255, 255)


class Pipeline:
    def __init__(self, pipeline: Vision | AmbientVision) -> None:
        self.pipeline: Vision | AmbientVision = pipeline

    def detect(self, image: numpy.ndarray) -> Vision.detect:
        """
        Process an image using a pipeline.

        Args:
            image: The image to apply the pipeline to.

        Returns:
            The pipeline output.
        """
        return self.pipeline.detect(image)

    def draw(self, image: numpy.ndarray, targets: Any, copy: bool = False) -> numpy.ndarray:
        """
        Draw the pipeline output on the image.

        Args:
            image: The image to draw on.
            targets: The pipeline output.
            copy: Whether to copy the image before drawing.

        Returns:
            The image with the pipeline output drawn on it.

        """
        if copy:
            image = image.copy()
        return self.draw_target(image, targets)

    def draw_contours(self, image, targets: List[numpy.ndarray]):

        return cv2.drawContours(image, targets, -1, color=DEFAULT_TARGET_COLOR,)