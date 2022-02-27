from matplotlib import pyplot as plt

from sensorsim import scenes
from sensorsim.cameras import Camera

scene = scenes.PhantomScene()
# scene.display()

camera = Camera(horizontalResolution=200)
image = camera.capture(scene)

plt.imshow(image)
plt.show()
