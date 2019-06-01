
import integ as it

from plotter import FrameData
from utils import MathUtils
from utils import PendulumMathUtils

import math


class PendulumAngleInteg:

    def __init__(self, mp, circle, m, g, dt, frame_dt_count):
        self._mp = mp
        self._circle = circle
        self._m = m
        self._g = g
        self._deq = None
        self._dt = dt
        self._frame_dt_count = frame_dt_count

    def init_deq(self, rho_max):
        radius = self._circle.get_radius()
        self._deq = it.RungeKutta4th(DiffEq(radius), rho_max, 0)

    def calculate_frame(self):

        rho, rhovel, _ = self._deq.execute(self._dt, self._frame_dt_count)

        m = self._m
        g = self._g

        mp = self._mp

        pos = self._circle.calc(rho)
        radius = self._circle.get_radius()
        vel = rhovel * radius

        # radial unit vector r1
        r1 = MathUtils.unit_vec_len(mp-pos, radius)

        # tangential unit vecotr t1
        t1 = MathUtils.unit_vec(MathUtils.orth_vec_z(r1, pos))

        if rho < 0:
            t1 = t1 * (-1)

        # - Forces

        # tangential force vector
        F_tan = PendulumMathUtils.tangential_force(m, g, rho) * t1

        # radial force vector
        F_zen = PendulumMathUtils.radial_force(m, vel, radius) * r1

        # total force vector
        F_tot = ( F_tan + F_zen )

        # - Energies

        # potential energy
        E_pot = PendulumMathUtils.potential_energy(m, g, rho, radius)

        # kinetic energy
        E_kin = PendulumMathUtils.kinetic_energy(g, vel)




        return FrameData(pos, mp, F_zen, F_tan, F_tot, E_pot, E_kin)


class DiffEq:

    def __init__(self, radius):
        self._radius = radius

    def f(self, pos, vel, t):
        return -(9.81/self._radius)*math.sin(pos)
