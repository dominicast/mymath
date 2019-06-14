
from enum import Enum

import math
import numpy as np


class Action(Enum):
    SHOW = 1
    HTML = 2


class Source:

    def __init__(self, pos, strength, color):
        self._pos = pos
        self._strength = strength
        self._color = color

    def get_pos(self):
        return self._pos

    def get_strength(self):
        return self._strength

    def get_size(self):
        return self._strength * 2

    def get_color(self):
        return self._color


class Magnet(Source):
    pass


class MountPoint(Source):
    pass


class Config:

    def __init__(self):

        self._width = None
        self._height = None
        self._distance = None

        self._mount_point = None
        self._magnets = None
        self._friction = None

        self._m = None

        self._abort_velocity = None
        self._min_steps = None
        self._max_steps = None

        self._dt = None    # [s]

        self._interval = None    # [ms]
        self._speed = None    # [1=realtime]
        self._frames = None
        self._action = None

        self._name = None

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

    def get_min_steps(self):
        return self._min_steps

    def get_max_steps(self):
        return self._max_steps

    def get_dt(self):
        return self._dt

    def get_interval(self):
        return self._interval

    def get_speed(self):
        return self._speed

    def get_frames(self):
        return self._frames

    def get_action(self):
        return self._action

    def get_name(self):
        return self._name


class BaseConfig:

    def _get_config(self):
        config = Config()

        config._distance = 0.02
        config._m = 1

        config._abort_velocity = 0.04
        config._min_steps = 1000
        config._max_steps = 500000

        config._dt = 0.001

        config._interval = 10
        config._speed = 1

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

        config._name = 'triangle'

        config._width = 1
        config._height = 1

        config._friction = 0.5

        config._mount_point = MountPoint(np.array([0, 0]), 0.1, 'k')

        magnets = [
            Magnet(BaseConfig._calc_positions(0.3, 90), 0.05, 'r'),
            Magnet(BaseConfig._calc_positions(0.3, 210), 0.05, 'g'),
            Magnet(BaseConfig._calc_positions(0.3, 330), 0.05, 'b')
        ]
        config._magnets = magnets

        config._action = action

        if config.get_action() == Action.HTML:
            config._frames = 64

        return config
