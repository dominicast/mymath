
import integ as it

import math
import numpy as np


class DiffEq:

    def __init__(self, G, m_u, m_v):
        self._G = G
        self._m_u = m_u
        self._m_v = m_v

    def f(self, pos, vel, t):

        G = self._G

        m_u = self._m_u
        m_v = self._m_v

        u = pos[0]
        v = pos[1]

        r = u - v
        r_len = math.sqrt(r[0]**2+r[1]**2+r[2]**2)

        factor = -G * ((m_u*m_v)/(r_len**3))

        F_v = factor * -r
        F_u = factor * r

        return np.array([F_u, F_v])


class Solver1:

    def __init__(self, u, v, G, dt):

        sp = np.concatenate((u.get_sp(), v.get_sp()), axis=0)
        sv = np.concatenate((u.get_sv(), v.get_sv()), axis=0)

        self._deq = it.RungeKutta4th(DiffEq(G, u.get_m(), v.get_m()), sp, sv)
        self._dt = dt

    def execute(self, t_delta):
        dt_count = round(t_delta / self._dt)
        pos, _, _, _ = self._deq.execute(self._dt, dt_count)
        return pos
