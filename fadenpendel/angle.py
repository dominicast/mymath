
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

        if rho < 0:
            rho = -rho

        # unit vectors
        r1, t1 = PendulumMathUtils.calculate_unit_vectors(mp, pos, radius)

        # forces
        F_tot, F_tan, F_zen = PendulumMathUtils.calculate_force_vectors(rho, radius, vel, m, g, t1, r1)

        # energies
        E_pot, E_kin = PendulumMathUtils.calculate_energies(rho, radius, vel, m, g)

        # return
        return FrameData(pos, mp, F_zen, F_tan, F_tot, E_pot, E_kin)


class DiffEq:

    def __init__(self, radius):
        self._radius = radius

    def f(self, pos, vel, t):
        return -(9.81/self._radius)*math.sin(pos)
