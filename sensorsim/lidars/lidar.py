import itertools
import math

import numpy as np

from pytissueoptics.scene import Vector
from pytissueoptics.scene.intersection import Ray, SimpleIntersectionFinder
from pytissueoptics.scene.intersection.intersectionFinder import Intersection
from pytissueoptics.scene.logger import Logger

from sensorsim.scenes.sensorScene import SensorScene
from sensorsim.light import UniformRaySource


class LiDAR(UniformRaySource):
    def __init__(self, position=Vector(0, 4, 0), direction=Vector(0, 0, -1), divergence=0.0,
                 xTheta: float = 360, yTheta: float = 90, xResolution: int = 512, yResolution: int = 128):
        self._attenuation = 1/40
        self._noise = 0.001
        self._divergence = divergence * np.pi / 180

        super().__init__(position, direction, xTheta, yTheta, xResolution, yResolution)

    def _createRayAt(self, xTheta: float, yTheta: float):
        if self._divergence == 0.0:
            super()._createRayAt(xTheta, yTheta)
        else:
            divergencePoints = [-self._divergence, 0, self._divergence]
            for (dx, dy) in itertools.product(divergencePoints, divergencePoints):
                super()._createRayAt(xTheta + dx, yTheta + dy)

    def propagate(self, scene: SensorScene, logger: Logger = None):
        intersectionFinder = SimpleIntersectionFinder(scene.solids)
        for ray in self._rays:
            intersection = intersectionFinder.findIntersection(ray)
            if not intersection:
                continue
            signal = self._measureSignal(ray, intersection)
            if logger:
                logger.logDataPoint(signal, intersection.position)

    def _measureSignal(self, ray: Ray, intersection: Intersection) -> float:
        intersection.position += ray.direction * self._distanceNoiseAt(intersection.distance)
        reflectance = intersection.polygon.insideMaterial.retroReflectionAt(ray.direction,
                                                                            normal=intersection.polygon.normal)
        return self._intensityAt(intersection.distance) * reflectance

    def _distanceNoiseAt(self, distance: float) -> Vector:
        return np.random.normal(0, self._noise) * distance

    def _intensityAt(self, distance: float) -> float:
        intensity = math.exp(-self._attenuation * distance)
        noise = np.random.normal(0, 5 * self._noise) * intensity
        return intensity + noise


class OusterLiDAR(LiDAR):
    def __init__(self, position=Vector(0, 4, 0), direction=Vector(0, 0, -1), xResolution: int = 512):
        super().__init__(position, direction, xTheta=360, yTheta=90, xResolution=xResolution, yResolution=128,
                         divergence=0.07)
