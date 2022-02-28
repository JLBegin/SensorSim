import numpy as np
from matplotlib import pyplot as plt

from pytissueoptics.scene import Vector
from sensorsim import scenes
from sensorsim.cameras import Camera

scene = scenes.PhantomScene()

camera = Camera(position=Vector(-1.5, 2, -1.5), direction=Vector(-1, 0, -1), horizontalResolution=640)
imageL = camera.capture(scene)

camera = Camera(position=Vector(1.5, 2, -1.5), direction=Vector(1, 0, -1), horizontalResolution=640)
imageR = camera.capture(scene)

fig, [axL, axR] = plt.subplots(1, 2)
vmax = np.max([imageL, imageR])
axL.imshow(imageL/vmax)
axR.imshow(imageR/vmax)
plt.show()
