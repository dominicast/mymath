
import integ as it

import time
import numpy as np
import math

from utils import FrameData


class Pendulum:

    def __init__(self, magnets, mount_point, friction, m, g, dt, speed, math_utils):
        self._magnets = magnets
        self._mount_point = mount_point
        self._friction = friction
        self._m = m
        self._g = g
        self._deq = None
        self._dt = dt
        self._speed = speed
        self._timestamp = None
        self._math_utils = math_utils

    def init_deq(self, sp, sv):

        magnets = self._magnets
        mount_point = self._mount_point
        friction = self._friction
        m = self._m
        g = self._g
        math_utils = self._math_utils

        self._deq = it.RungeKutta4th(DiffEq(magnets, mount_point, friction, m, g, math_utils), sp, sv)

    def calculate_frame(self):

        ts = time.time()
        if self._timestamp is None:
            self._timestamp = ts
            return None
        frame_dt = (ts - self._timestamp) * self._speed
        self._timestamp = ts

        dt_count = round(frame_dt / self._dt)

        # ---

        pos, vel, _, t = self._deq.execute(self._dt, dt_count)

        # ---

        mp = self._mount_point.get_pos()
        m = self._m

        return FrameData(pos, mp, m)


class DiffEq:

    def __init__(self, magnets, mount_point, friction, m, g, math_utils):
        self._magnets = magnets
        self._mount_point = mount_point
        self._friction = friction
        self._m = m
        self._g = g
        self._math_utils = math_utils

    def f(self, pos, vel, t):

        math_utils = self._math_utils

        # -- acting forces

        # gravity

        fg = self._m * self._g
        fg_v = np.array([0, 0, -fg])

        # magnets and mount-point

        mv_v = []

        sources = self._magnets + [self._mount_point]
        for source in sources:
            dv = source.get_pos() - pos
            square_dist = dv[0]**2 + dv[1]**2 + dv[2]**2
            fm = source.get_strength() / square_dist
            fm_v_n = math_utils.unit_vec_ps(dv) * fm
            mv_v.append(fm_v_n)

        # friction

        square_vel = vel[0]**2 + vel[1]**2 + vel[2]**2
        if square_vel > 0:
            ff = square_vel * self._friction
            ff_v = math_utils.unit_vec_v(vel) * ff * (-1)
        else:
            ff_v = np.array([0, 0, 0])

        # total force

        fw_v = fg_v + ff_v
        for f in mv_v:
            fw_v += f

        # -- mount corrections

        mp = self._mount_point.get_pos()
        r = pos - mp
        theta, phi = self._math_utils.spherical_coords_mp(r)

        # x correction

        x = math.sin(phi)**2 + math.cos(phi)**2 * math.cos(theta)**2
        y = (-1) * math.sin(phi) * math.cos(phi) + math.cos(phi) * math.cos(theta)**2 * math.sin(phi)
        z = math.cos(phi) * math.cos(theta) * math.sin(theta)

        fx_v = fw_v[0] * np.array([x, y, z])

        # y correction

        x = (-1) * math.cos(phi) * math.sin(phi) + math.sin(phi) * math.cos(theta)**2 * math.cos(phi)
        y = math.cos(phi)**2 + math.sin(phi)**2 * math.cos(theta)**2
        z = math.sin(phi) * math.cos(theta) * math.sin(theta)

        fy_v = fw_v[1] * np.array([x, y, z])

        # z correction

        x = math.sin(theta) * math.cos(theta) * math.cos(phi)
        y = math.sin(theta) * math.cos(theta) * math.sin(phi)
        z = math.sin(theta)**2

        fz_v = fw_v[2] * np.array([x, y, z])

        f_v = fx_v + fy_v + fz_v

        # -- centripetal force

        square_vel = vel[0]**2 + vel[1]**2 + vel[2]**2
        dv = mp - pos
        radius = math.sqrt(dv[0]**2 + dv[1]**2 + dv[2]**2)
        fc = (self._m * square_vel) / radius
        fc_v = self._math_utils.unit_vec_r(dv) * fc

        f_v = f_v + fc_v

        # -- return

        return f_v / self._m
