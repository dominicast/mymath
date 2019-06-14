
import integ as it

import time
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

    def __init__(self, magnets, mount_point, distance, friction, m, abort_velocity, min_steps, max_steps, dt, speed):
        self._magnets = magnets
        self._mount_point = mount_point
        self._distance = distance
        self._friction = friction
        self._m = m

        self._abort_velocity = abort_velocity
        self._min_steps = min_steps
        self._max_steps = max_steps

        self._deq = None
        self._dt = dt
        self._speed = speed

        self._timestamp = None
        self._done = False

    def init_deq(self, sp, sv):

        magnets = self._magnets
        mount_point = self._mount_point
        distance = self._distance
        friction = self._friction
        m = self._m

        self._deq = it.RungeKutta4th(DiffEq(magnets, mount_point, distance, friction, m), sp, sv)

    def calculate_frame(self):

        if self._done:
            return None

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

        n = round(t/self._dt)
        sources = self._magnets + [ self._mount_point ]
        norm_vel = la.norm(vel)

        found = False
        closest_source = None
        closest_source_dist = None

        # check for stop condition

        if n < self._min_steps:
            return FrameData(self._done, pos, found, closest_source, closest_source_dist)

        if norm_vel <= self._abort_velocity:
            for src in sources:
                r = pos - src.get_pos()
                if la.norm(r) < src.get_size():
                    found = True
                    break

        if not found and n < self._max_steps:
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
