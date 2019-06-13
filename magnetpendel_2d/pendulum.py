
import integ as it

import math
import numpy as np
import numpy.linalg as la

from plotter import FrameData


class Pendulum:

    def __init__(self, magnets, mount_point, distance, friction, m, dt, frame_dt_count):
        self._magnets = magnets
        self._mount_point = mount_point
        self._distance = distance
        self._friction = friction
        self._m = m
        self._deq = None
        self._dt = dt
        self._frame_dt_count = frame_dt_count

    def init_deq(self, sp, sv):

        magnets = self._magnets
        mount_point = self._mount_point
        distance = self._distance
        friction = self._friction
        m = self._m

        self._deq = it.RungeKutta4th(DiffEq(magnets, mount_point, distance, friction, m), sp, sv)

    def calculate_frame(self):

        pos, vel, _, t = self._deq.execute(self._dt, self._frame_dt_count)

        return FrameData(pos)

        #mp = self._mp
        #m = self._m
        #g = self._g
        #friction = self._friction

        #E_pot, E_kin, F_tot, F_zen, F_tan, F_d, _, _ = PendulumMath(pos, vel, mp, m, g, friction).calculate_ext()

        #return FrameData(pos, mp, m, F_zen, F_tan, F_d, F_tot, E_pot, E_kin)


class DiffEq:

    def __init__(self, magnets, mount_point, distance, friction, m):
        self._magnets = magnets
        self._mount_point = mount_point
        self._distance = distance
        self._friction = friction
        self._m = m

    def f(self, pos, vel, t):

        mount_point = self._mount_point
        friction = self._friction
        m = self._m
        distance = self._distance

        total_force = np.array([0,0])

        # magnet forces
        for magnet in self._magnets:
            r = pos - magnet.get_pos()
            dist = math.sqrt(r[0]**2 + r[1]**2 + distance**2)
            force = (magnet.get_strength() / dist**3) * r
            total_force = total_force - force

        # restoring force
        r = pos - mount_point.get_pos()
        force = mount_point.get_strength() * r
        total_force = total_force - force

        # friction force
        total_force = total_force - vel * friction

        # acceleration from froce (a = F/m)
        acceleration = total_force / m

        return acceleration


class Observer:

    def __init__(self, cfg):
        self._cfg = cfg

        self._done = False
        self._found = False
        self._closest_src = None
        self._closest_src_dist = 0
        self._n = 0
        self._len = 0

    def _step_done(self, pos, n):
        pass

    def _process_done(self, pos, n, found):
        pass

    def notify(self, pos, vel, t, n):

        if self._done:
            return True

        if self._step_done(pos, n):
            return True

        # update _len

        norm_vel = la.norm(vel)

        self._len += norm_vel

        # check for stop condition

        if n < self._cfg.m_nMinSteps:
            return

        found = False
        if norm_vel <= self._cfg.m_fAbortVel:
            for src in self._cfg.sources:
                r = pos - src.get_pos()
                if la.norm(r) < src.get_size():
                    found = True
                    break

        if not found and n < self._cfg.m_nMaxSteps:
            return

        # stop condition satisfied
        # calculate some values

        self._n = n
        self._found = found

        closest_dist = None

        for src in self._cfg.sources:

            r = pos - src.get_pos()

            dist = math.sqrt(math.pow(r[0], 2) + math.pow(r[1], 2) + math.pow(self._cfg.m_fHeight, 2))

            if (closest_dist is None) or (dist < closest_dist):
                closest_dist = dist
                self._closest_src = src
                self._closest_src_dist = dist

        self._done = True

        self._process_done(pos, n, found)

        return True

    def get_done(self):
        return self._done

    def get_found(self):
        return self._found

    def get_n(self):
        return self._n

    def get_len(self):
        return self._len

    def get_closest_src(self):
        return self._closest_src

    def get_closest_src_dist(self):
        return self._closest_src_dist
