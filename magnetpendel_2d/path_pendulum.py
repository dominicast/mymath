
from pendulum import Pendulum

import time


class PathPendulum(Pendulum):

    def __init__(self, magnets, mount_point, distance, friction, m, abort_velocity, min_steps, max_steps, dt, speed):
        super().__init__(magnets, mount_point, distance, friction, m, abort_velocity, min_steps, max_steps, dt)
        self._speed = speed
        self._timestamp = None

    def start(self):
        self._timestamp = time.time()

    def calculate_frame(self):

        ts = time.time()

        if self._timestamp is None:
            self._timestamp = ts
            return None

        frame_dt = (ts - self._timestamp) * self._speed

        self._timestamp = ts

        dt_count = round(frame_dt / self._dt)

        return super().calculate_frame(dt_count)
