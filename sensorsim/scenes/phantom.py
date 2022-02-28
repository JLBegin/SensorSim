from pytissueoptics.scene import *
from sensorsim.light import Light

from sensorsim.materials import *
from sensorsim.scenes.sensorScene import SensorScene


class PhantomScene(SensorScene):
    _baseMaterial = Concrete()
    ROOM = []
    CROSSWALK = []
    OBJECTS = []
    SIGN = []

    def __init__(self):
        self._create()
        self._solids = [*self.ROOM, *self.CROSSWALK, *self.OBJECTS, *self.SIGN]
        self._light = Light(Vector(0, 8, 0))

    def addToViewer(self, viewer: MayaviViewer):
        viewer.add(*self.ROOM[:-1], representation="surface", colormap="bone")
        viewer.add(self.ROOM[-1], representation="surface", colormap="bone", reverseColormap=True)
        viewer.add(*self.CROSSWALK, *self.OBJECTS, *self.SIGN, representation="surface", colormap="Set2",
                   reverseColormap=True, constantColor=True)

    @property
    def solids(self):
        return self._solids

    @property
    def light(self):
        # todo: rename to lighting when proper lighting object will exist
        return self._light

    def _create(self):
        self.ROOM = self._room()
        self.CROSSWALK = self._crossWalk()
        self.OBJECTS = self._objects()
        self.SIGN = self._sign()

    def _room(self):
        w, d, h, t = 20, 20, 8, 0.1
        floor = Cuboid(w + t, t, d + t, position=Vector(0, -t / 2, 0), material=self._baseMaterial)
        leftWall = Cuboid(t, h, d, position=Vector(-w / 2, h / 2, 0), material=self._baseMaterial)
        rightWall = Cuboid(t, h, d, position=Vector(w / 2, h / 2, 0), material=self._baseMaterial)
        backWall = Cuboid(w, h, t, position=Vector(0, h / 2, -d / 2), material=self._baseMaterial)
        return [floor, leftWall, rightWall, backWall]

    def _crossWalk(self):
        return [Cuboid(0.7, 0.001, 4, position=Vector(i, 0, -8), material=ReflectivePaint()) for i in range(-5, 5)]

    def _objects(self):
        cubeA = Cube(3, position=Vector(-5, 3/2, -6), material=Plywood())
        cubeB = Cube(3, position=Vector(5, 3/2, -6), material=Plywood())
        cubeB.rotate(0, 20, 0)
        cubeC = Cube(1, position=Vector(-5, 3.866, -6), material=ReflectivePaint())
        cubeC.rotate(0, 0, 45)
        cubeC.rotate(45, 0, 0)
        sphere = Sphere(0.75, order=2, position=Vector(5, 3.75, -6), material=Chrome())
        return [cubeA, cubeB, cubeC, sphere]

    def _sign(self):
        sign = Cuboid(1.5, 1.5, 0.001, position=Vector(7.8, 5, -5 + (0.1 + 0.01)/2), material=ReflectiveFilm())
        sign.rotate(0, 0, 45)
        stand = Cuboid(0.1, 5, 0.1, position=Vector(7.8, 2.5, -5), material=StainlessSteel())
        return [sign, stand]
