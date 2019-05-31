
import integ as it

from plotter import FrameData

import numpy as np
import math


class ForceImpl:

    def __init__(self, mp, sp, m, g):
        self._mp = mp
        self._sp = sp
        self._m = m
        self._g = g

    def create_deq(self):
        return it.RungeKutta4th(DiffEq(self._mp, self._m, self._g), self._sp, np.array([0, 0, 0]))

    def create_frame(self, integ_ctx):
        return AnimationFrame(integ_ctx, self._mp, self._m, self._g)


class ForceMath:

    def __init__(self, pos, vel, mp, m, g):
        self._pos = pos
        self._vel = vel
        self._mp = mp
        self._m = m
        self._g = g

    # calculate vector length of vec
    @staticmethod
    def vec_len(vec):
        return math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)

    # calculate unit vector of vec given it's length
    @staticmethod
    def unit_vec_len(vec, len):
        return vec / len

    # calculate unit vector of vec
    def unit_vec(self, vec):
        return vec / self.vec_len(vec)

    # calcuate vector orthogonal to vec
    # pointing from pos towards the z-axis
    @staticmethod
    def orth_vec_z(vec, pos):
        z = pos[2]
        x = -(vec[2] * z / (vec[0] + vec[1] * (pos[1] / pos[0])))
        y = (pos[1] / pos[0]) * x
        return np.array([x, y, z])

    # calculate the angle between vec and the z-axis
    @staticmethod
    def z_angle(vec):
        return math.acos(0 * vec[0] + 0 * vec[1] + -1 * vec[2])

    def calculate(self):

        m = self._m
        g = self._g

        mp = self._mp

        pos = self._pos
        vel = self.vec_len(self._vel)

        # radius
        radius = self.vec_len(pos-mp)

        # radial unit vector r1
        r1 = self.unit_vec_len(mp-pos, radius)

        # tangential unit vecotr t1
        t1 = self.unit_vec(self.orth_vec_z(r1, pos))

        # displacement
        rho = self.z_angle(-r1)

        # tangential force
        # F_tan = m * g * sin(rho)
        F_tan = - m * g * math.sin(rho) * t1

        # radial force
        # F_zen = ( m * v^2 ) / radius
        F_zen = ((m * vel**2)/radius) * r1

        # F_tot
        F_tot = (F_tan+F_zen)

        return F_tot, F_zen, F_tan, rho, radius

    def calculate_ext(self):

        m = self._m
        g = self._g

        vel = self.vec_len(self._vel)

        F_tot, F_zen, F_tan, rho, radius = self.calculate()

        # potential energy
        # E_pot = m * g * l * (1 - cos(rho))
        E_pot = m * g * (radius - (radius * math.cos(rho)))

        #kinetic energy
        # E_kin = (1/2) * m * v^2
        E_kin = (1/2) * g * math.pow(vel, 2)

        return E_pot, E_kin, F_tot, F_zen, F_tan, rho, radius


class DiffEq:

    def __init__(self, mp, m, g):
        self._mp = mp
        self._m = m
        self._g = g

    def f(self, pos, vel, t):
        F_tot, _, _, _, _ = ForceMath(pos, vel, self._mp, self._m, self._g).calculate()
        return F_tot


class AnimationFrame:

    def __init__(self, integ_ctx, mp, m, g):
        self._integ_ctx = integ_ctx
        self._mp = mp
        self._m = m
        self._g = g

    def perform(self):

        mp = self._mp
        m = self._m
        g = self._g

        pos, vel, _ = self._integ_ctx.get_deq().execute(self._integ_ctx.get_dt(), self._integ_ctx.get_count())

        E_pot, E_kin, F_tot, F_zen, F_tan, _, _ = ForceMath(pos, vel, mp, m, g).calculate_ext()

        return FrameData(pos, mp, F_zen, F_tan, F_tot, E_pot, E_kin)
