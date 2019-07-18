
from scipy.integrate import solve_ivp

import math
import numpy as np


class Solver3:

    def __init__(self, u, v, G, dt):

        self._sp_u = u.get_sp()[0]
        self._sv_u = u.get_sv()[0]
        self._sp_v = v.get_sp()[0]
        self._sv_v = v.get_sv()[0]

        self._G = G
        self._m_u = u.get_m()
        self._m_v = v.get_m()

    def f(self, t, y):

        G = self._G
        m_u = self._m_u
        m_v = self._m_v

        u_pos = np.array([y[0], y[1], y[2]])
        u_vel = np.array([y[3], y[4], y[5]])
        v_pos = np.array([y[6], y[7], y[8]])
        v_vel = np.array([y[9], y[10], y[11]])

        r = u_pos - v_pos
        r_len = math.sqrt(r[0] ** 2 + r[1] ** 2 + r[2] ** 2)

        factor = -G * ((m_u * m_v) / (r_len ** 3))

        F_v = factor * -r
        F_u = factor * r

        u_pos_d = u_vel
        u_vel_d = F_u
        v_pos_d = v_vel
        v_vel_d = F_v

        return np.array([u_pos_d[0], u_pos_d[1], u_pos_d[2], u_vel_d[0], u_vel_d[1], u_vel_d[2], v_pos_d[0], v_pos_d[1], v_pos_d[2], v_vel_d[0], v_vel_d[1], v_vel_d[2]])

    def execute(self, t_delta):

        sp_u = self._sp_u
        sv_u = self._sv_u
        sp_v = self._sp_v
        sv_v = self._sv_v

        sp = np.array([sp_u[0], sp_u[1], sp_u[2], sv_u[0], sv_u[1], sv_u[2], sp_v[0], sp_v[1], sp_v[2], sv_v[0], sv_v[1], sv_v[2]])

        sol = solve_ivp(self.f, [0, t_delta], sp, t_eval=[t_delta], method='RK45', vectorized=True)

        y = sol.y

        u_pos = np.array([y[0][0], y[1][0], y[2][0]])
        u_vel = np.array([y[3][0], y[4][0], y[5][0]])
        v_pos = np.array([y[6][0], y[7][0], y[8][0]])
        v_vel = np.array([y[9][0], y[10][0], y[11][0]])

        self._sp_u = u_pos
        self._sv_u = u_vel
        self._sp_v = v_pos
        self._sv_v = v_vel

        result = np.array([u_pos, v_pos])

        return result
