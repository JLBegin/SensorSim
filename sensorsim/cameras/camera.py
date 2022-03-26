import math
from enum import Enum

import numpy as np

from pytissueoptics.scene import Vector
from pytissueoptics.scene.intersection import SimpleIntersectionFinder, Ray
from pytissueoptics.scene.intersection.intersectionFinder import Intersection
from sensorsim.light import UniformRaySource, Light
from sensorsim.scenes.sensorScene import SensorScene


class AspectRatio(Enum):
    FOUR_THIRDS = 4/3
    WIDESCREEN = 16/9


class Camera(UniformRaySource):
    def __init__(self, position=Vector(0, 4, 0), direction=Vector(0, 0, -1), horizontalFOV: float = 120,
                 horizontalResolution: int = 640, aspectRatio: AspectRatio = AspectRatio.FOUR_THIRDS):
        super().__init__(position, direction, horizontalFOV, horizontalFOV/aspectRatio.value,
                         horizontalResolution, int(horizontalResolution/aspectRatio.value))

    def capture(self, scene: SensorScene) -> np.ndarray:
        intersectionFinder = SimpleIntersectionFinder(scene)
        pixels = []
        for ray in self._rays:
            intersection = intersectionFinder.findIntersection(ray)
            if not intersection:
                pixels.append((0, 0, 0))
                continue
            pixels.append(self._measurePixel(ray, intersection, scene.light))
        image = np.reshape(pixels, (*self._resolution, 3))
        image = np.fliplr(np.rot90(image))
        return image

    def _measurePixel(self, ray: Ray, intersection: Intersection, light: Light) -> list:
        lightDirection = intersection.position - light.position
        distance = lightDirection.getNorm()
        lightDirection.normalize()
        reflectance = intersection.polygon.insideMaterial.reflectionAt(viewDirection=ray.direction,
                                                                       lightDirection=lightDirection,
                                                                       normal=intersection.polygon.normal)
        attenuation = 1/distance
        reflectance *= attenuation
        return [c*reflectance for c in intersection.polygon.insideMaterial.color]
