
import integ as it

import time
import math

from utils import FrameData
from utils import MathUtils
from utils import PendulumMathUtils


class PendulumForceInteg:

    def __init__(self, mp, m, g, friction, speed):
        self._mp = mp
        self._m = m
        self._g = g
        self._friction = friction
        self._deq = None
        self._speed = speed
        self._timestamp = None

    def init_deq(self, sp, sv, dt):
        #self._deq = it.RungeKutta4th(DiffEq(self._mp, self._m, self._g, self._friction), sp, sv, dt)
        self._deq = it.SciPy(DiffEq(self._mp, self._m, self._g, self._friction), sp, sv)

    def calculate_frame(self):

        ts = time.time()
        if self._timestamp is None:
            self._timestamp = ts
            return None
        frame_dt = (ts - self._timestamp) * self._speed
        self._timestamp = ts

        # ---

        pos, vel, _, t = self._deq.process_td(frame_dt)

        # ---

        mp = self._mp
        m = self._m
        g = self._g
        friction = self._friction

        E_pot, E_kin, F_tot, F_zen, F_tan, F_d, _, _ = PendulumMath(pos, vel, mp, m, g, friction).calculate_ext()

        return FrameData(pos, mp, m, F_zen, F_tan, F_d, F_tot, E_pot, E_kin)


class DiffEq:

    def __init__(self, mp, m, g, friction):
        self._mp = mp
        self._m = m
        self._g = g
        self._friction = friction

    def f(self, pos, vel, t):
        F_tot, _, _, _, _, _ = PendulumMath(pos, vel, self._mp, self._m, self._g, self._friction).calculate()
        return F_tot/self._m


class PendulumMath:

    def __init__(self, pos, vel, mp, m, g, friction):
        self._pos = pos
        self._vel = vel
        self._mp = mp
        self._m = m
        self._g = g
        self._friction = friction

    @staticmethod
    def _sign(n):
        if n >= 0:
            return 1
        else:
            return -1

    @staticmethod
    def _angle_sign(pos, mp):
        dx = pos[0] - mp[0]
        dy = pos[1] - mp[1]
        if dx == 0 and dy == 0:
            return 1
        if dx == 0:
            return PendulumMath._sign(dy)
        if dy == 0:
            return PendulumMath._sign(dx)
        return PendulumMath._sign(dx)

    # calculate the angle between vec and the z-axis
    @staticmethod
    def _z_angle(vec, pos, mp):
        sign = PendulumMath._angle_sign(pos, mp)
        return math.acos(0 * vec[0] + 0 * vec[1] + -1 * vec[2]) * sign

    # calculate the velocity value and sign
    @staticmethod
    def _velocity(vec):
        len = MathUtils.vec_len(vec)
        if vec[0] == 0 and vec[1] == 0:
            return len
        if vec[0] != 0:
            if vec[0] >= 0:
                return len
            else:
                return -len
        else:
            if vec[1] >= 0:
                return len
            else:
                return -len

    def calculate(self):

        m = self._m
        g = self._g
        friction = self._friction

        mp = self._mp

        pos = self._pos
        radius = MathUtils.vec_len(pos - mp)
        vel = PendulumMath._velocity(self._vel)

        # unit vectors
        r1, t1, v1 = PendulumMathUtils.calculate_unit_vectors(mp, pos, radius, self._vel)

        # displacement
        rho = PendulumMath._z_angle(-r1, pos, mp)

        # forces
        F_tot, F_tan, F_zen, F_d = PendulumMathUtils.calculate_force_vectors(rho, radius, vel, m, g, friction, t1, r1, v1)

        # return
        return F_tot, F_zen, F_tan, F_d, rho, radius

    def calculate_ext(self):

        m = self._m
        g = self._g

        vel = MathUtils.vec_len(self._vel)

        F_tot, F_zen, F_tan, F_d, rho, radius = self.calculate()

        # energies
        E_pot, E_kin = PendulumMathUtils.calculate_energies(rho, radius, vel, m, g)

        # return
        return E_pot, E_kin, F_tot, F_zen, F_tan, F_d, rho, radius
