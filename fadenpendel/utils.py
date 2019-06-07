
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
        len = MathUtils.vec_len(vec)
        if len == 0:
            return vec
        return vec / len

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
        return - m * g * math.sin(abs(rho))

    # F_zen = ( m * v^2 ) / radius
    @staticmethod
    def radial_force(m, vel, radius):
        return (m * vel**2)/radius

    # F_d = friction * v^2
    @staticmethod
    def friction_force(friction, vel):
        return friction * vel**2

    # E_pot = m * g * l * (1 - cos(rho))
    @staticmethod
    def potential_energy(m, g, rho, radius):
        return m * g * (radius - (radius * math.cos(abs(rho))))

    # E_kin = (1/2) * m * v^2
    @staticmethod
    def kinetic_energy(g, vel):
        return (1/2) * g * vel**2

    # calculate unit vectors t1 and r1
    # r1: radial unit vector pointing from pos to the mount point
    # t1: tangential unit vector orthogonal to r1 pointing from pos towards the z-axis
    @staticmethod
    def calculate_unit_vectors(mp, pos, radius, vel):

        # radial unit vector r1
        r1 = MathUtils.unit_vec_len(mp-pos, radius)

        # tangential unit vecotr t1
        t1 = MathUtils.unit_vec(MathUtils.orth_vec_z(r1, pos))

        # vilocity unit vecotr v1
        if vel is not None:
            v1 = MathUtils.unit_vec(vel)
        else:
            v1 = None

        return r1, t1, v1

    # calculate force vectors F_tan, F_zen, F_tot
    @staticmethod
    def calculate_force_vectors(rho, radius, vel, m, g, friction, t1, r1, v1):

        # tangential force vector
        F_tan = PendulumMathUtils.tangential_force(m, g, rho) * t1

        # radial force vector
        F_zen = PendulumMathUtils.radial_force(m, vel, radius) * r1

        # friction vector
        F_d = PendulumMathUtils.friction_force(friction, vel) * (-v1)

        # F_tot
        F_tot = (F_tan+F_zen+F_d)

        return F_tot, F_tan, F_zen, F_d

    # calculate energies E_pot and E_kin
    @staticmethod
    def calculate_energies(rho, radius, vel, m, g):

        # potential energy
        E_pot = PendulumMathUtils.potential_energy(m, g, rho, radius)

        # kinetic energy
        E_kin = PendulumMathUtils.kinetic_energy(g, vel)

        return E_pot, E_kin
