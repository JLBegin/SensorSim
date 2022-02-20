from pytissueoptics.scene import MayaviViewer
from pytissueoptics.scene.logger import Logger
from sensorsim.scenes.phantom import SensorScene
from sensorsim.source import Source


class Sensor:
    def __init__(self, source: Source = Source()):
        self._logger = Logger()
        self._source = source
        self._scene = None

    def capture(self, scene: SensorScene):
        self._scene = scene
        self._source.propagate(scene, logger=self._logger)

    def display(self, showScene=True, showSensor=True):
        mViewer = MayaviViewer()
        mViewer.addLogger(self._logger, colormap="inferno", reverseColormap=False)
        if showScene:
            self._scene.addToViewer(mViewer)
        if showSensor:
            self._scene.addSensorToViewer(mViewer)
        mViewer.show()
