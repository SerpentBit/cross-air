from typing import Any, Callable

import numpy
from ovl import Vision


class Pipeline:
    def __init__(self, pipeline: Vision, draw_target: Callable) -> None:
        self.pipeline: Vision = pipeline
        self.draw_target: Callable = draw_target

    def detect(self, image: numpy.ndarray) -> Any:
        """
        Process an image using a pipeline.

        Args:
            image: The image to apply the pipeline to.

        Returns:
            The pipeline output.
        """
        return self.pipeline.detect(image)

    def draw(self, image: numpy.ndarray, targets: Any, copy:  bool = False) -> numpy.ndarray:
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
