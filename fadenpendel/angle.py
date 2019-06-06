
import integ as it

from plotter import FrameData
from utils import PendulumMathUtils

import math
import numpy as np


class PendulumAngleInteg:

    def __init__(self, mp, circle, m, g, friction, dt, frame_dt_count):
        self._mp = mp
        self._circle = circle
        self._m = m
        self._g = g
        self._friction = friction
        self._deq = None
        self._dt = dt
        self._frame_dt_count = frame_dt_count

    def init_deq(self, rho_max):
        radius = self._circle.get_radius()
        friction = self._friction
        self._deq = it.RungeKutta4th(DiffEq(radius, friction, self._m, self._g), rho_max, 0)

    def calculate_frame(self):

        rho, rhovel, _, t = self._deq.execute(self._dt, self._frame_dt_count)

        m = self._m
        g = self._g
        friction = self._friction

        mp = self._mp

        pos = self._circle.calc(rho)
        radius = self._circle.get_radius()
        vel = rhovel * radius

        # unit vectors
        r1, t1, v1 = PendulumMathUtils.calculate_unit_vectors(mp, pos, radius, np.array([0,0,0]))

        # forces
        F_tot, F_tan, F_zen, F_d = PendulumMathUtils.calculate_force_vectors(rho, radius, vel, m, g, friction, t1, r1, v1)

        # energies
        E_pot, E_kin = PendulumMathUtils.calculate_energies(rho, radius, vel, m, g)

        # return
        return FrameData(pos, mp, m, F_zen, F_tan, F_d, F_tot, E_pot, E_kin)


class DiffEq:

    def __init__(self, radius, friction, m, g):
        self._radius = radius
        self._friction = friction
        self._m = m
        self._g = g

    def f(self, pos, vel, t):
        m = self._m
        g = self._g
        radius = self._radius
        friction = self._friction

        if vel >= 0:
            vel_direction = 1
        else:
            vel_direction = -1

        result = -(g / radius) * math.sin(pos) - (radius * vel_direction * friction * (vel**2))/m

        return result
