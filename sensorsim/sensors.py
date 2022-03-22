from typing import List

import numpy as np
from matplotlib import pyplot as plt

from pytissueoptics.scene import MayaviViewer, Vector
from pytissueoptics.scene.logger import Logger
from sensorsim.cameras import Camera
from sensorsim.lidars import LiDAR
from sensorsim.scenes.phantom import SensorScene


class Sensor:
    def capture(self, scene: SensorScene):
        raise NotImplementedError

    def display(self, showScene=False, showSensor=False):
        raise NotImplementedError


class ScanningSensor(Sensor):
    def __init__(self, source: LiDAR = LiDAR()):
        self._logger = Logger()
        self._source = source
        self._scene = None

    def capture(self, scene: SensorScene):
        self._scene = scene
        self._source.propagate(scene, logger=self._logger)

    def display(self, showScene=False, showSensor=False):
        mViewer = MayaviViewer()
        mViewer.addLogger(self._logger, colormap="inferno", reverseColormap=False)
        if showScene:
            self._scene.addToViewer(mViewer)
        if showSensor:
            self._scene.addSensorToViewer(mViewer)
        mViewer.show()


class SensorSuite(Sensor):
    def __init__(self, lidars=[], radars=[], cameras=[]):
        self._lidars = lidars
        self._radars = radars
        self._cameras = cameras
        self._scene = None
        self._images = []

    def capture(self, scene: SensorScene):
        self._scene = scene
        for sensor in self._sensors:
            image = sensor.capture(scene)
            if image is not None:
                self._images.append(image)

    @property
    def _sensors(self) -> List[Sensor]:
        return [*self._lidars, *self._radars, *self._cameras]

    def display(self, showScene=False, showSensor=False):
        for lidar in self._lidars:
            lidar.display(showScene=showScene, showSensor=showSensor)
        for radar in self._radars:
            radar.display(showScene=showScene, showSensor=showSensor)

        if len(self._images) == 0:
            return

        fig, axes = plt.subplots(1, len(self._images))
        vmax = np.max(self._images) * 1.2
        for i, image in enumerate(self._images):
            axes[i].imshow(image / vmax)
        plt.show()


class AVSuite(SensorSuite):
    def __init__(self, position=Vector(0, 0, 0)):
        self._position = position
        lidar360 = ScanningSensor(source=LiDAR(position=Vector(0, 4, 0) + self._position))
        # frontLeftCamera = Camera(position=Vector(-1.5, 2, -1.5) + self._position, direction=Vector(-1, 0, -1),
        #                          horizontalResolution=640, horizontalFOV=120)
        # frontRightCamera = Camera(position=Vector(1.5, 2, -1.5) + self._position, direction=Vector(1, 0, -1),
        #                           horizontalResolution=640, horizontalFOV=120)
        super().__init__(lidars=[lidar360]) # , cameras=[frontLeftCamera, frontRightCamera])
