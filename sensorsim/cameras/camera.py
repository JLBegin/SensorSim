import math
from enum import Enum

import numpy as np

from pytissueoptics.scene import Vector
from pytissueoptics.scene.intersection import SimpleIntersectionFinder, Ray
from pytissueoptics.scene.intersection.intersectionFinder import Intersection
from sensorsim.light import UniformRaySource
from sensorsim.scenes.sensorScene import SensorScene


class Color(Enum):
    RED = (1, 0, 0)
    GREEN = (0, 1, 0)
    BLUE = (0, 0, 1)
    WHITE = (1, 1, 1)
    BLACK = (0, 0, 0)


class AspectRatio(Enum):
    FOUR_THIRDS = 4/3
    WIDESCREEN = 16/9


class Camera(UniformRaySource):
    def __init__(self, position=Vector(2, 2, -2), direction=Vector(1, 0, -1), horizontalFOV: float = 150,
                 horizontalResolution: int = 640, aspectRatio: AspectRatio = AspectRatio.FOUR_THIRDS):
        super().__init__(position, direction, horizontalFOV, horizontalFOV/aspectRatio.value,
                         horizontalResolution, int(horizontalResolution/aspectRatio.value))

    def capture(self, scene: SensorScene) -> np.ndarray:
        intersectionFinder = SimpleIntersectionFinder(scene.solids)
        pixels = []
        for ray in self._rays:
            intersection = intersectionFinder.findIntersection(ray)
            if not intersection:
                pixels.append((0, 0, 0))
                continue
            pixels.append(self._measurePixel(ray, intersection))
        image = np.reshape(pixels, (*self._resolution, 3))
        image = np.fliplr(np.rot90(image))
        # image = np.moveaxis(image, 0, 1)
        return image

    def _measurePixel(self, ray: Ray, intersection: Intersection) -> tuple:
        surfaceNormal = intersection.polygon.normal
        angle = math.acos(-surfaceNormal.dot(ray.direction))

        reflectance = intersection.polygon.insideMaterial.retroReflectionAt(angle)
        # fixme: switch to reflection(sourceAngle, viewAngle)
        return reflectance, reflectance, reflectance
