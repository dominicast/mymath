
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


class MathUtils:

    # calculate vector length of vec
    @staticmethod
    def vec_len(vec):
        return math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)

    # calculate unit vector of vec given it's length
    @staticmethod
    def unit_vec_len(vec, len):
        return vec / len

    # calculate unit vector of vec
    @staticmethod
    def unit_vec(vec):
        return vec / MathUtils.vec_len(vec)

    # calcuate vector orthogonal to vec
    # pointing from pos towards the z-axis
    @staticmethod
    def orth_vec_z(vec, pos):
        z = pos[2]
        x = -(vec[2] * z / (vec[0] + vec[1] * (pos[1] / pos[0])))
        y = (pos[1] / pos[0]) * x
        return np.array([x, y, z])


class PendulumMathUtils:

    # F_tan = m * g * sin(rho)
    @staticmethod
    def tangential_force(m, g, rho):
        return - m * g * math.sin(rho)

    # F_zen = ( m * v^2 ) / radius
    @staticmethod
    def radial_force(m, vel, radius):
        return (m * vel**2)/radius

    # E_pot = m * g * l * (1 - cos(rho))
    @staticmethod
    def potential_energy(m, g, rho, radius):
        return m * g * (radius - (radius * math.cos(rho)))

    # E_kin = (1/2) * m * v^2
    @staticmethod
    def kinetic_energy(g, vel):
        return (1/2) * g * vel**2
