
import integ as it

from plotter import FrameData

import numpy as np
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

        mp = self._mp
        circle = self._circle
        radius = circle.get_radius()
        m = self._m
        g = self._g




        # - position of the pendulum

        pos = circle.calc(rho)

        # - radialer einheitsvektor e_r

        e_r = (mp - pos) / radius

        # - tangentialer einheitsvektor e_t

        z = pos[2]
        x = -(e_r[2] * z / (e_r[0] + e_r[1] * (pos[1] / pos[0])))
        y = (pos[1] / pos[0]) * x

        e_t = np.array([x, y, z])

        if rho < 0:
            e_t = e_t * (-1)

        e_t = e_t / math.sqrt(math.pow(e_t[0], 2) + math.pow(e_t[1], 2) + math.pow(e_t[2], 2))

        # - velocity

        vel =rhovel * radius

        # - Energies

        # E_pot = m * g * l * (1 - cos(rho))
        E_pot = m * g * (radius - (radius * math.cos(rho)))

        # E_kin = (1/2) * m * v^2
        E_kin = (1/2) * g * math.pow(vel, 2)

        # - Forces

        # F_tan = m * g * sin(rho)
        F_tan = - m * g * math.sin(rho) * e_t

        # F_zen = ( m * v^2 ) / radius
        F_zen = ( ( m * math.pow(vel, 2) ) / radius ) * e_r

        # F_tot = F_tan + F_zen
        F_tot = ( F_tan + F_zen )



        return FrameData(pos, mp, F_zen, F_tan, F_tot, E_pot, E_kin)


class DiffEq:

    def __init__(self, radius):
        self._radius = radius

    def f(self, pos, vel, t):
        return -(9.81/self._radius)*math.sin(pos)
