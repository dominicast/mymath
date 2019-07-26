
from enum import Enum

import math
import numpy as np


class Action(Enum):
    SHOW = 1
    HTML = 2


class Source:

    def __init__(self, pos, strength, size, color):
        self._pos = pos
        self._strength = strength
        self._size = size
        self._color = color

    def get_pos(self):
        return self._pos

    def get_strength(self):
        return self._strength

    def get_size(self):
        return self._size

    def get_color(self):
        return self._color


class Magnet(Source):
    pass


class MountPoint(Source):
    pass


class Config:

    def __init__(self):

        self._name = None

        self._width = None
        self._height = None
        self._distance = None

        self._mount_point = None
        self._magnets = None
        self._friction = None

        self._m = None

        self._abort_velocity = None
        self._t_min = None
        self._t_max = None

        self._dt = None    # [s]

        # path config

        self._start_pos = None
        self._start_vel = None
        self._interval = None    # [ms]
        self._speed = None    # [1=realtime]
        self._frames = None
        self._action = None

        # pattern config

        self._worker_count = None
        self._point_size = None
        self._point_delta = None
        self._dt_chunk_size = None

    def get_name(self):
        return self._name

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_distance(self):
        return self._distance

    def get_mount_point(self):
        return self._mount_point

    def get_magnets(self):
        return self._magnets

    def get_friction(self):
        return self._friction

    def get_m(self):
        return self._m

    def get_abort_velocity(self):
        return self._abort_velocity

    def get_t_min(self):
        return self._t_min

    def get_t_max(self):
        return self._t_max

    def get_dt(self):
        return self._dt

    def get_start_pos(self):
        return self._start_pos

    def get_start_vel(self):
        return self._start_vel

    def get_interval(self):
        return self._interval

    def get_speed(self):
        return self._speed

    def get_frames(self):
        return self._frames

    def get_action(self):
        return self._action

    def get_worker_count(self):
        return self._worker_count

    def get_point_size(self):
        return self._point_size

    def get_point_delta(self):
        return self._point_delta

    def get_dt_chunk_size(self):
        return self._dt_chunk_size


class BaseConfig:

    def _get_config(self):
        config = Config()

        # general config

        config._distance = 0.025
        config._m = 1

        config._abort_velocity = 0.04

        config._dt = 0.0025
        config._t_min = 1000 * config._dt
        config._t_max = 500000 * config._dt

        # path config

        config._interval = 20
        config._speed = 1

        # pattern config

        config._worker_count = 10
        config._point_size = 5
        config._dt_chunk_size = 10

        # return

        return config

    @staticmethod
    def _calc_positions(radius, angle):
        x = radius * math.cos(angle * (math.pi / 180))
        y = radius * math.sin(angle * (math.pi / 180))
        pos = np.array([x, y])
        return pos


class TriangleConfig(BaseConfig):

    def get_config(self, action):
        config = super()._get_config()

        # general config

        config._name = 'triangle'

        config._width = 1
        config._height = 1

        config._friction = 0.2

        config._mount_point = MountPoint(np.array([0, 0]), 0.8, 0.0025, 'k')

        magnets = [
            Magnet(BaseConfig._calc_positions(0.425, 90), 0.025, 0.025, 'r'),
            Magnet(BaseConfig._calc_positions(0.425, 210), 0.025, 0.025, 'g'),
            Magnet(BaseConfig._calc_positions(0.425, 330), 0.025, 0.025, 'b')
        ]
        config._magnets = magnets

        # path config

        config._start_pos = np.array([1, 1])
        config._start_vel = np.array([0, 0])

        config._action = action

        if config.get_action() == Action.HTML:
            config._frames = 350

        # pattern config

        config._point_delta = 0.0125

        # return

        return config
