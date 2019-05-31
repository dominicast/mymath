
import math
import numpy as np


class Circle:

    def __init__(self, radius, mp, phi):
        self._radius = radius
        self._mp = mp
        self._phi = phi

    def calc(self, rho):
        # Kuegelkoordinaten

        x = self._radius * math.sin(rho) * math.cos(self._phi)
        y = self._radius * math.sin(rho) * math.sin(self._phi)
        z = self._radius * math.cos(rho)

        v = np.array([x, y, z])
        v[2] = -v[2]
        v = self._mp + v

        return v

    def get_radius(self):
        return self._radius
