import itertools
import math
from typing import List

import numpy as np

from pytissueoptics.scene import Vector
from pytissueoptics.scene.intersection import Ray, SimpleIntersectionFinder
from pytissueoptics.scene.intersection.intersectionFinder import Intersection
from pytissueoptics.scene.logger import Logger

from sensorsim.scenes.sensorScene import SensorScene


class Source:
    def __init__(self, position=Vector(0, 4, 0), direction=Vector(0, 0, -1), divergence=0.0,
                 xTheta: float = 360, yTheta: float = 90, xResolution: int = 512, yResolution: int = 128):
        self._position = position
        self._direction = direction
        self._theta = (xTheta * np.pi / 180, yTheta * np.pi / 180)
        self._resolution = (xResolution, yResolution)
        self._rays = []

        self._attenuation = 1/40
        self._noise = 0.001
        self._divergence = divergence * np.pi / 180

        self._createRays()

    def _createRays(self):
        for xTheta in self._getXThetaRange():
            for yTheta in self._getYThetaRange():
                if self._divergence == 0.0:
                    self._createRayAt(xTheta, yTheta)
                else:
                    divergencePoints = [-self._divergence, 0, self._divergence]
                    for (dx, dy) in itertools.product(divergencePoints, divergencePoints):
                        self._createRayAt(xTheta+dx, yTheta+dy)

    def _getXThetaRange(self) -> List[float]:
        return np.linspace(0, self._theta[0], self._resolution[0]) - self._theta[0] / 2

    def _getYThetaRange(self) -> List[float]:
        return np.linspace(0, self._theta[1], self._resolution[1]) - self._theta[1] / 2

    def _createRayAt(self, xTheta: float, yTheta: float):
        rayDirection = Vector(-math.sin(xTheta), 0, -math.cos(xTheta))
        rayDirection.add(Vector(0, math.tan(yTheta), 0))
        rayDirection.normalize()
        self._rays.append(Ray(self._position, rayDirection))

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

        surfaceNormal = intersection.polygon.normal
        angle = math.acos(-surfaceNormal.dot(ray.direction))
        reflectance = intersection.polygon.insideMaterial.retroReflectionAt(angle)
        return self._intensityAt(intersection.distance) * reflectance

    def _distanceNoiseAt(self, distance: float) -> Vector:
        return np.random.normal(0, self._noise) * distance

    def _intensityAt(self, distance: float) -> float:
        intensity = math.exp(-self._attenuation * distance)
        noise = np.random.normal(0, 5 * self._noise) * intensity
        return intensity + noise


class OusterLiDAR(Source):
    def __init__(self, position=Vector(0, 4, 0), direction=Vector(0, 0, -1), xResolution: int = 512):
        super().__init__(position, direction, xTheta=360, yTheta=90, xResolution=xResolution, yResolution=128,
                         divergence=0.07)
