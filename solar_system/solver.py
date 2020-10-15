
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

        p_u = pos[0]
        p_v = pos[1]

        r = p_v - p_u
        r_len = math.sqrt(r[0]**2+r[1]**2+r[2]**2)

        factor = G * ((m_u*m_v)/(r_len**3))

        F_u = factor * r
        F_v = factor * -r

        a_u = (F_u/m_u)
        a_v = (F_v/m_v)

        return np.array([a_u, a_v])


class Solver:

    def __init__(self, bodies, G, logger=None):

        u = bodies[0]
        v = bodies[1]

        sp = np.concatenate((u.get_sp(), v.get_sp()), axis=0)
        sv = np.concatenate((u.get_sv(), v.get_sv()), axis=0)

        #self._deq = it.RungeKutta4th(DiffEq(u.get_m(), v.get_m()), sp, sv, 10)
        self._deq = it.SciPy(DiffEq(G, u.get_m(), v.get_m()), sp, sv, None, logger)

    def process(self, t_delta):
        pos, _, _, _ = self._deq.process_td(t_delta)
        return pos
