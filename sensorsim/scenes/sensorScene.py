from typing import List

from pytissueoptics.scene import *
from pytissueoptics.scene.solids import Solid
from sensorsim.light import Light


class SensorScene(Scene):
    def __init__(self):
        super().__init__(ignoreIntersections=True)

    @property
    def light(self) -> Light:
        raise NotImplementedError

    def addToViewer(self, viewer: MayaviViewer):
        raise NotImplementedError

    def addSensorToViewer(self, viewer: MayaviViewer):
        viewer.add(*self._sensorGraphics, representation="surface", colormap="bone")

    @property
    def _sensorGraphics(self) -> List[Solid]:
        sensor = Sphere(0.3, order=2, position=Vector(0, 4, 0))
        podA = Cuboid(0.07, 4, 0.07, position=Vector(0, 2, 0))
        return [sensor, podA]

    def display(self):
        viewer = MayaviViewer()
        self.addToViewer(viewer)
        viewer.show()
