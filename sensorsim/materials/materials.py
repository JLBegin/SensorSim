import math

from pytissueoptics.scene import Material, Vector


class DiffuseMaterial(Material):
    def __init__(self, reflectance: float = 0.30, roughness: float = 0.7, specularIntensity: float = 50):
        assert 0.0 <= reflectance <= 1.0
        assert 0.0 <= roughness <= 1.0
        self._R = reflectance
        self._kd = roughness
        self._ks = 1 - roughness
        self._n = specularIntensity

    def retroReflectionAt(self, lightDirection: Vector, normal: Vector) -> float:
        """ Using Blinn-Phong illumination model without ambient lighting and view angle same as illumination angle
        for a single light source. Input angle is between surface normal and illumination, in radians. """
        return self.reflectionAt(viewDirection=lightDirection, lightDirection=lightDirection, normal=normal)

    def reflectionAt(self, viewDirection: Vector, lightDirection: Vector, normal: Vector) -> float:
        """ Using Blinn-Phong illumination model without ambient lighting for a single light source.
        Expects viewDirection and lightDirection to point towards the surface (negative dot product with normal). """
        R = self._getReflected(lightDirection, normal)
        diffuseReflection = self._kd * (-normal.dot(lightDirection))
        specularReflection = self._ks * (-R.dot(viewDirection))**self._n
        return self._R * (diffuseReflection + specularReflection)

    @staticmethod
    def _getIncidenceAngle(vector: Vector, normal: Vector) -> float:
        """ Expects dot product to be negative. """
        return math.acos(-normal.dot(vector))

    @staticmethod
    def _getReflected(vector: Vector, normal: Vector):
        return vector - normal * 2 * vector.dot(normal)


class ReflectiveFilm(DiffuseMaterial):
    """ https://www.researchgate.net/publication/251610177_Photographic_assessment_of_retroreflective_film_properties. """
    def __init__(self, reflectance=0.58):
        super().__init__(reflectance=reflectance)

    def retroReflectionAt(self, lightDirection: Vector, normal: Vector) -> float:
        return self._R * (-normal.dot(lightDirection)) ** 0.5

    @staticmethod
    def _getReflected(vector: Vector, normal: Vector):
        return vector * -1


class ReflectivePaint(DiffuseMaterial):
    def __init__(self, reflectance=0.4):
        super().__init__(reflectance=reflectance)

    def retroReflectionAt(self, lightDirection: Vector, normal: Vector) -> float:
        return self._R * (-normal.dot(lightDirection)) ** 0.8

    @staticmethod
    def _getReflected(vector: Vector, normal: Vector):
        return vector * -1


class Concrete(DiffuseMaterial):
    def __init__(self):
        super().__init__(reflectance=0.25)


class StainlessSteel(DiffuseMaterial):
    def __init__(self):
        super().__init__(reflectance=0.5, roughness=0.5)
