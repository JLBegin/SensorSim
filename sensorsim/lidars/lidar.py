import itertools
import math
import time

import numpy as np

from pytissueoptics.scene import Vector
from pytissueoptics.scene.intersection import Ray, SimpleIntersectionFinder
from pytissueoptics.scene.intersection.intersectionFinder import Intersection, FastIntersectionFinder
from pytissueoptics.scene.logger import Logger
from pytissueoptics.scene.tree.treeConstructor.binary import SAHBasicKDTreeConstructor, \
    ShrankBoxSAHWideAxisTreeConstructor, BalancedKDTreeConstructor, SAHWideAxisTreeConstructor

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
        t0 = time.time()
        intersectionFinder = FastIntersectionFinder(scene)

        t1 = time.time()
        print(f"Tree construction time: {round(t1-t0, 2)}s")

        # self._rays = UniformRaySource(Vector(0, 4, 0), Vector(0, 0, -1), 180, 0, xResolution=100, yResolution=1)._rays

        missedRays = 0
        for ray in self._rays:
            intersection = intersectionFinder.findIntersection(ray)
            if not intersection:
                missedRays += 1
                continue
            signal = self._measureSignal(ray, intersection)
            if logger:
                logger.logDataPoint(signal, intersection.position)

        t2 = time.time()
        print(f"Tracing time: {round(t2-t1, 2)}s")
        print(f"Missed {missedRays} rays")  # Expected 25552 miss with default LiDAR

    def _measureSignal(self, ray: Ray, intersection: Intersection) -> float:
        intersection.position += ray.direction * self._distanceNoiseAt(intersection.distance)
        if intersection.polygon.insideMaterial is None:
            return 1
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
