from dataclasses import dataclass

from pytissueoptics.scene import Vector


@dataclass
class Light:
    position: Vector


# class Lighting:
#     def __init__(self):
#         self._lights = []
