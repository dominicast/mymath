
import math
import numpy as np


class FrameData:

    def __init__(self, pos, mp, m):
        self._pos = pos
        self._mp = mp
        self._m = m

    def get_pos(self):
        return self._pos

    def get_mp(self):
        return self._mp

    def get_m(self):
        return self._m


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


class MathUtilsDl:

    @staticmethod
    def _xy_to_rad(ol, al):

        if al == 0:
            if ol >= 0:
                return math.pi/2
            else:
                return 3*math.pi/2

        angle = math.atan(abs(ol/al))

        if al >= 0:
            if ol >= 0:
                return angle
            else:
                return (2*math.pi)-angle
        else:
            if ol >= 0:
                return math.pi - angle
            else:
                return math.pi + angle

    def unit_vec_ps(self, vec):

        ol = math.sqrt(vec[0]**2 + vec[1]**2)
        al = -vec[2]
        alpha = self._xy_to_rad(ol, al)

        ol = vec[1]
        al = vec[0]
        beta = self._xy_to_rad(ol, al)

        x = math.cos(alpha) * math.cos(beta)
        y = math.cos(alpha) * math.sin(beta)
        z = -math.sin(alpha)

        return np.array([x, y, z])

    def unit_vec_v(self, vec):

        ol = vec[2]
        al = math.sqrt(vec[0]**2 + vec[1]**2)
        phi = self._xy_to_rad(ol, al)

        ol = vec[1]
        al = vec[0]
        epsilon = self._xy_to_rad(ol, al)

        x = math.cos(phi) * math.cos(epsilon)
        y = math.cos(phi) * math.sin(epsilon)
        z = math.sin(phi)

        return np.array([x, y, z])

    def unit_vec_r(self, vec):

        vec = -vec

        theta, phi = self.spherical_coords_mp(vec)

        x = (-1) * math.sin(theta) * math.cos(phi)
        y = (-1) * math.sin(theta) * math.sin(phi)
        z = math.cos(theta)

        return np.array([x, y, z])

    def spherical_coords_mp(self, vec):
        ol = math.sqrt(vec[0]**2 + vec[1]**2)
        al = -vec[2]
        gamma = self._xy_to_rad(ol, al)

        ol = vec[1]
        al = vec[0]
        delta = self._xy_to_rad(ol, al)

        return gamma, delta
