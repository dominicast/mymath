
import integ as it

from plotter import FrameData
from utils import MathUtils
from utils import PendulumMathUtils


class PendulumForceInteg:

    def __init__(self, mp, m, g, dt, frame_dt_count):
        self._mp = mp
        self._m = m
        self._g = g
        self._deq = None
        self._dt = dt
        self._frame_dt_count = frame_dt_count

    def init_deq(self, sp, sv):
        self._deq = it.RungeKutta4th(DiffEq(self._mp, self._m, self._g), sp, sv)

    def calculate_frame(self):

        pos, vel, _ = self._deq.execute(self._dt, self._frame_dt_count)

        mp = self._mp
        m = self._m
        g = self._g

        E_pot, E_kin, F_tot, F_zen, F_tan, _, _ = PendulumMath(pos, vel, mp, m, g).calculate_ext()

        return FrameData(pos, mp, F_zen, F_tan, F_tot, E_pot, E_kin)


class DiffEq:

    def __init__(self, mp, m, g):
        self._mp = mp
        self._m = m
        self._g = g

    def f(self, pos, vel, t):
        F_tot, _, _, _, _ = PendulumMath(pos, vel, self._mp, self._m, self._g).calculate()
        return F_tot


class PendulumMath:

    def __init__(self, pos, vel, mp, m, g):
        self._pos = pos
        self._vel = vel
        self._mp = mp
        self._m = m
        self._g = g

    def calculate(self):

        m = self._m
        g = self._g

        mp = self._mp

        pos = self._pos
        radius = MathUtils.vec_len(pos - mp)
        vel = MathUtils.vec_len(self._vel)

        # unit vectors
        r1, t1 = PendulumMathUtils.calculate_unit_vectors(mp, pos, radius)

        # displacement
        rho = MathUtils.z_angle(-r1)

        # forces
        F_tot, F_tan, F_zen = PendulumMathUtils.calculate_force_vectors(rho, radius, vel, m, g, t1, r1)

        # return
        return F_tot, F_zen, F_tan, rho, radius

    def calculate_ext(self):

        m = self._m
        g = self._g

        vel = MathUtils.vec_len(self._vel)

        F_tot, F_zen, F_tan, rho, radius = self.calculate()

        # energies
        E_pot, E_kin = PendulumMathUtils.calculate_energies(rho, radius, vel, m, g)

        # return
        return E_pot, E_kin, F_tot, F_zen, F_tan, rho, radius
