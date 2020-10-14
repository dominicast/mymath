
import integ as it

import math
import numpy as np


class DiffEq:

    def __init__(self, m_u, m_v):
        self._m_u = m_u
        self._m_v = m_v

    def f(self, pos, vel, t):

        G = 6.6743*pow(10,-11)

        m_u = self._m_u
        m_v = self._m_v

        p_u = pos[0]
        p_v = pos[1]

        r = p_v - p_u
        r_len = math.sqrt(r[0]**2+r[1]**2+r[2]**2)

        print(p_u)

        factor = G * ((m_u*m_v)/(r_len**3))

        F_u = factor * r
        F_v = factor * -r

        a_u = (F_u/m_u)
        a_v = (F_v/m_u)

        return np.array([a_u, a_v])


class Solver:

    def __init__(self, bodies, dt, logger=None):

        u = bodies[0]
        v = bodies[1]

        sp = np.concatenate((u.get_sp(), v.get_sp()), axis=0)
        sv = np.concatenate((u.get_sv(), v.get_sv()), axis=0)

        #self._deq = it.RungeKutta4th(DiffEq(u.get_m(), v.get_m()), sp, sv, dt)
        self._deq = it.SciPy(DiffEq(u.get_m(), v.get_m()), sp, sv, None, logger)

    def process(self, t_delta):
        pos, _, _, _ = self._deq.process_td(t_delta)
        return pos
