import math

from pytissueoptics.scene import Material, Vector
from sensorsim.materials.colors import Color


class DiffuseMaterial(Material):
    def __init__(self, reflectance: float = 0.30, roughness: float = 0.7, specularIntensity: float = 10,
                 color: Color = Color.GRAY):
        assert 0.0 <= reflectance <= 1.0
        assert 0.0 <= roughness <= 1.0
        self._R = reflectance
        self._kd = roughness
        self._ks = 1 - roughness
        self._ka = 0.1
        self._n = specularIntensity
        self._color = color.value

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
        return self._R * (diffuseReflection + specularReflection) + self._ka

    @staticmethod
    def _getIncidenceAngle(vector: Vector, normal: Vector) -> float:
        """ Expects dot product to be negative. """
        return math.acos(-normal.dot(vector))

    @staticmethod
    def _getReflected(vector: Vector, normal: Vector):
        return vector - normal * 2 * vector.dot(normal)

    @property
    def color(self):
        return self._color


class ReflectiveFilm(DiffuseMaterial):
    """ https://www.researchgate.net/publication/251610177_Photographic_assessment_of_retroreflective_film_properties. """
    def __init__(self):
        super().__init__(reflectance=0.58, roughness=0.4, specularIntensity=5, color=Color.SAFETY_YELLOW)

    def retroReflectionAt(self, lightDirection: Vector, normal: Vector) -> float:
        return self._R * (-normal.dot(lightDirection)) ** 0.5

    @staticmethod
    def _getReflected(vector: Vector, normal: Vector):
        return vector * -1


class ReflectivePaint(DiffuseMaterial):
    def __init__(self):
        super().__init__(reflectance=0.45, roughness=0.6, specularIntensity=10, color=Color.SAFETY_YELLOW)

    def retroReflectionAt(self, lightDirection: Vector, normal: Vector) -> float:
        p = normal.dot(lightDirection)
        if p > 0:
            print("Positive dot")
            return 0

        return self._R * (-p) ** 0.5

    @staticmethod
    def _getReflected(vector: Vector, normal: Vector):
        return vector * -1


class Concrete(DiffuseMaterial):
    def __init__(self):
        super().__init__(reflectance=0.3, color=Color.SILVER)


class StainlessSteel(DiffuseMaterial):
    def __init__(self):
        super().__init__(reflectance=0.4, roughness=0.6, color=Color.SILVER)


class Chrome(DiffuseMaterial):
    def __init__(self):
        super().__init__(reflectance=0.60, roughness=0.3, color=Color.CHROME)


class Plywood(DiffuseMaterial):
    def __init__(self):
        super().__init__(reflectance=0.35, color=Color.WOOD)
