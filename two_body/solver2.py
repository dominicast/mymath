
import integ1o as it

import math
import numpy as np


class DiffEq:

    def __init__(self, G, m_u, m_v):
        self._G = G
        self._m_u = m_u
        self._m_v = m_v

    def f(self, pos, t):

        G = self._G

        m_u = self._m_u
        m_v = self._m_v

        u_pos = pos[0]
        u_vel = pos[1]
        v_pos = pos[2]
        v_vel = pos[3]

        r = u_pos - v_pos
        r_len = math.sqrt(r[0]**2+r[1]**2+r[2]**2)

        factor = -G * ((m_u*m_v) / (r_len**3))

        F_v = factor * -r
        F_u = factor * r

        u_pos_d = u_vel
        u_vel_d = F_u
        v_pos_d = v_vel
        v_vel_d = F_v

        return np.array([u_pos_d, u_vel_d, v_pos_d, v_vel_d])


class Solver2:

    def __init__(self, u, v, G, dt):

        sp_u = u.get_sp()[0]
        sv_u = u.get_sv()[0]
        sp_v = v.get_sp()[0]
        sv_v = v.get_sv()[0]

        sp = np.array([sp_u, sv_u, sp_v, sv_v])

        #self._deq = it.SciPy(DiffEq(G, u.get_m(), v.get_m()), sp)
        self._deq = it.RungeKutta4th(DiffEq(G, u.get_m(), v.get_m()), sp, dt)

    def process(self, t_delta):
        pos, _, _ = self._deq.process_td(t_delta)
        result = np.array([pos[0], pos[2]])
        return result
