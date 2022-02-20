from sensorsim import Sensor, scenes

scene = scenes.PhantomScene()
lidar = Sensor()

lidar.capture(scene)

lidar.display()
