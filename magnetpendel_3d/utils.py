
import math
import numpy as np


class MathUtils:

    def _spherical_coords(self, vec):
        r = math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
        theta = math.acos(vec[2] / r)
        phi = math.atan2(vec[1], vec[0])
        return theta, phi

    def spherical_coords_mp(self, vec):
        r = np.array([vec[0], vec[1], vec[2]])
        r[2] = -r[2]
        return self._spherical_coords(r)


class MathUtilsVec(MathUtils):

    @staticmethod
    def _unit_vec(vec):
        vec_len = math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
        if vec_len == 0:
            raise Exception('Unknown vector lengeth')
        return vec / vec_len

    def unit_vec_ps(self, vec):
        return self._unit_vec(vec)

    def unit_vec_v(self, vec):
        return self._unit_vec(vec)

    def unit_vec_r(self, vec):
        return self._unit_vec(vec)


class MathUtilsSc(MathUtils):

    def _unit_vec(self, vec):
        theta, phi = self._spherical_coords(vec)
        x = math.sin(theta) * math.cos(phi)
        y = math.sin(theta) * math.sin(phi)
        z = math.cos(theta)
        return np.array([x, y, z])

    def unit_vec_ps(self, vec):
        return self._unit_vec(vec)

    def unit_vec_v(self, vec):
        return self._unit_vec(vec)

    def unit_vec_r(self, vec):
        return self._unit_vec(vec)
