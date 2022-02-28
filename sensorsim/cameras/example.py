from matplotlib import pyplot as plt

from pytissueoptics.scene import Vector
from sensorsim import scenes
from sensorsim.cameras import Camera

scene = scenes.PhantomScene()
# scene.display()

camera = Camera(position=Vector(-1.5, 2, -1.5), direction=Vector(-1, 0, -1), horizontalResolution=200)
image = camera.capture(scene)

plt.imshow(image)
plt.show()

camera = Camera(position=Vector(1.5, 2, -1.5), direction=Vector(1, 0, -1), horizontalResolution=200)
image = camera.capture(scene)

plt.imshow(image)
plt.show()
