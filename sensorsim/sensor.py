from pytissueoptics.scene import MayaviViewer
from pytissueoptics.scene.logger import Logger
from sensorsim.lidars import LiDAR
from sensorsim.scenes.phantom import SensorScene


class Sensor:
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
