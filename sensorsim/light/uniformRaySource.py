import math
from typing import List

import numpy as np

from pytissueoptics.scene import Vector
from pytissueoptics.scene.intersection import Ray


class UniformRaySource:
    def __init__(self, position, direction, xTheta: float, yTheta: float, xResolution: int, yResolution: int):
        self._position = position
        self._direction = direction
        self._theta = (xTheta * np.pi / 180, yTheta * np.pi / 180)
        self._resolution = (xResolution, yResolution)
        self._rays = []

        self._createRays()

    def _createRays(self):
        for xTheta in self._getXThetaRange():
            for yTheta in self._getYThetaRange():
                self._createRayAt(xTheta, yTheta)

    def _getXThetaRange(self) -> List[float]:
        return np.linspace(0, self._theta[0], self._resolution[0]) - self._theta[0] / 2

    def _getYThetaRange(self) -> List[float]:
        return np.linspace(0, self._theta[1], self._resolution[1]) - self._theta[1] / 2

    def _createRayAt(self, xTheta: float, yTheta: float):
        self._rays.append(Ray(self._position, self._getRayDirectionAt(xTheta, yTheta)))

    @staticmethod
    def _getRayDirectionAt(xTheta, yTheta) -> Vector:
        rayDirection = Vector(-math.sin(xTheta), 0, -math.cos(xTheta))
        rayDirection.add(Vector(0, math.tan(yTheta), 0))
        rayDirection.normalize()
        return rayDirection
