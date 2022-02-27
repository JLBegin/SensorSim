from sensorsim import Sensor, scenes
from sensorsim.lidars import LiDAR

scene = scenes.PhantomScene()
scene.display()

lidar = Sensor(source=LiDAR())

lidar.capture(scene)

lidar.display()
