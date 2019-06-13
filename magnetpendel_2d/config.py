
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

        self._time_factor = None

        self._integ_dt = None    # [s]
        self._integ_count = None
        self._integ_freq = None   # [ms]

        self._action = None

        self._frames = None

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

    def get_time_factor(self):
        return self._time_factor

    def get_friction(self):
        return self._friction

    def get_m(self):
        return self._m

    def get_integ_dt(self):
        return self._integ_dt

    def get_integ_count(self):
        return self._integ_count

    def get_integ_freq(self):
        return self._integ_freq

    def get_action(self):
        return self._action

    def get_frames(self):
        return self._frames

    def get_name(self):
        return self._name


class BaseConfig:

    def _get_config(self):
        config = Config()

        config._distance = 10
        config._m = 1

        config._time_factor = 1

        config._integ_dt = 0.01
        config._integ_count = 10
        config._integ_freq = 100

        return config

    @staticmethod
    def _calc_positions(width, height, radius, angle):
        x = width / 2 + radius * math.cos(angle * (math.pi / 180))
        y = height / 2 + radius * math.sin(angle * (math.pi / 180))
        pos = np.array([x, y])
        return pos


class TriangleConfig(BaseConfig):

    def get_config(self, action):
        config = super()._get_config()

        config._name = 'triangle'

        config._width = 800
        config._height = 800

        config._friction = 0.0005

        config._mount_point = MountPoint(BaseConfig._calc_positions(config.get_width(), config.get_height(), 0, 0), 0.000005, 'k')

        magnets = [
            Magnet(BaseConfig._calc_positions(config.get_width(), config.get_height(), 170, 90), 10, 'r'),
            Magnet(BaseConfig._calc_positions(config.get_width(), config.get_height(), 170, 210), 10, 'g'),
            Magnet(BaseConfig._calc_positions(config.get_width(), config.get_height(), 170, 330), 10, 'b')
        ]
        config._magnets = magnets

        config._action = action

        if config.get_action() == Action.HTML:
            config._frames = 64

        return config
