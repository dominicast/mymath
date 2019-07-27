
import integ as it

import math
import numpy as np
import numpy.linalg as la


class FrameData:

    def __init__(self, done, pos, found, source, dist):

        self._done = done

        self._pos = pos

        self._found = found
        self._source = source
        self._dist = dist

    def get_done(self):
        return self._done

    def get_pos(self):
        return self._pos

    def get_found(self):
        return self._found

    def get_source(self):
        return self._source

    def get_dist(self):
        return self._dist


class Pendulum:

    def __init__(self, magnets, mount_point, distance, friction, m, abort_velocity, t_min, t_max):
        self._magnets = magnets
        self._mount_point = mount_point
        self._distance = distance
        self._friction = friction
        self._m = m

        self._abort_velocity = abort_velocity
        self._t_min = t_min
        self._t_max = t_max

        self._deq = None

        self._done = False

    def init_deq(self, sp, sv, dt):

        magnets = self._magnets
        mount_point = self._mount_point
        distance = self._distance
        friction = self._friction
        m = self._m

        self._deq = it.SciPy(DiffEq(magnets, mount_point, distance, friction, m), sp, sv, max_step=dt)
        #self._deq = it.RungeKutta4th(DiffEq(magnets, mount_point, distance, friction, m), sp, sv, dt)

    def calculate_frame(self, frame_dt):

        if self._done:
            return None

        # ---

        pos, vel, _, t = self._deq.process_td(frame_dt)

        # ---

        sources = self._magnets + [ self._mount_point ]
        norm_vel = la.norm(vel)

        found = False
        closest_source = None
        closest_source_dist = None

        # check for stop condition

        if t < self._t_min:
            return FrameData(self._done, pos, found, closest_source, closest_source_dist)

        if norm_vel <= self._abort_velocity:
            for src in sources:
                r = pos - src.get_pos()
                if la.norm(r) < src.get_size():
                    found = True
                    break

        if not found and t < self._t_max:
            return FrameData(self._done, pos, found, closest_source, closest_source_dist)

        # find the closest source

        for src in sources:

            r = pos - src.get_pos()

            dist = math.sqrt(r[0]**2 + r[1]**2 + self._distance**2)

            if (closest_source_dist is None) or (dist < closest_source_dist):
                closest_source = src
                closest_source_dist = dist

        # done

        self._done = True

        return FrameData(self._done, pos, found, closest_source, closest_source_dist)


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
