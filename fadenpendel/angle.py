
import integ as it

import time
import math

from utils import FrameData
from utils import PendulumMathUtils


class PendulumAngleInteg:

    def __init__(self, mp, circle, m, g, friction, speed):
        self._mp = mp
        self._circle = circle
        self._m = m
        self._g = g
        self._friction = friction
        self._deq = None
        self._speed = speed
        self._timestamp = None

    def init_deq(self, rho_max, dt):
        radius = self._circle.get_radius()
        friction = self._friction
        #self._deq = it.RungeKutta4th(DiffEq(radius, friction, self._m, self._g), rho_max, 0, dt)
        self._deq = it.SciPy(DiffEq(radius, friction, self._m, self._g), rho_max, 0, max_step=dt)

    def calculate_frame(self):

        ts = time.time()
        if self._timestamp is None:
            self._timestamp = ts
            return None
        frame_dt = (ts - self._timestamp) * self._speed
        self._timestamp = ts

        # ---

        rho, rhovel, _, t = self._deq.process_td(frame_dt)

        # ---

        m = self._m
        g = self._g
        friction = self._friction

        mp = self._mp

        pos = self._circle.calc(rho)
        radius = self._circle.get_radius()
        vel = rhovel * radius

        # unit vectors
        r1, t1, _ = PendulumMathUtils.calculate_unit_vectors(mp, pos, radius, None)
        if rho * rhovel >= 0:
            v1 = t1
        else:
            v1 = -t1

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

    def f(self, rho, rhovel, t):
        m = self._m
        g = self._g
        radius = self._radius
        friction = self._friction

        G_t = - m * g * math.sin(rho)

        if rhovel >= 0:
            vel_direction = 1
        else:
            vel_direction = -1

        vel = rhovel * radius

        D = - vel_direction * PendulumMathUtils.friction_force(friction, vel)

        return (G_t+D)/(m*radius)
