from sensorsim import AVSuite, scenes

scene = scenes.PhantomScene()
scene.display()

sensors = AVSuite()
sensors.capture(scene)
sensors.display()
