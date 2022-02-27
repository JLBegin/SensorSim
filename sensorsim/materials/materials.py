import math

from pytissueoptics.scene import Material


class DiffuseMaterial(Material):
    def __init__(self, reflectance: float = 0.30, roughness: float = 0.7, specularIntensity: float = 50):
        assert 0.0 <= reflectance <= 1.0
        assert 0.0 <= roughness <= 1.0
        self._R = reflectance
        self._kd = roughness
        self._ks = 1 - roughness
        self._n = specularIntensity

    def retroReflectionAt(self, angle: float) -> float:
        """ Using Blinn-Phong illumination model without ambient lighting and view angle same as illumination angle
        for a single light source. Input angle is between surface normal and illumination, in radians. """
        diffuseReflection = self._kd * math.cos(angle)
        specularReflection = self._ks * math.cos(angle)**self._n
        return self._R * (diffuseReflection + specularReflection)


class ReflectiveFilm(DiffuseMaterial):
    """ https://www.researchgate.net/publication/251610177_Photographic_assessment_of_retroreflective_film_properties. """
    def __init__(self, reflectance=0.58):
        super().__init__(reflectance=reflectance)

    def retroReflectionAt(self, angle: float) -> float:
        return self._R * math.cos(angle) ** 0.5


class ReflectivePaint(DiffuseMaterial):
    def __init__(self, reflectance=0.4):
        super().__init__(reflectance=reflectance)

    def retroReflectionAt(self, angle: float) -> float:
        return self._R * math.cos(angle) ** 0.8


class Concrete(DiffuseMaterial):
    def __init__(self):
        super().__init__(reflectance=0.25)


class StainlessSteel(DiffuseMaterial):
    def __init__(self):
        super().__init__(reflectance=0.5, roughness=0.5)
