
from enum import Enum
from utils import *


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
        self._width = None
        self._height = None
        self._depth = None

        self._mount_point = None

        self._start_pos = None
        self._start_vel = None

        self._magnets = None

        self._m = None
        self._g = None

        self._friction = None
        self._disturbance = None

        self._dt = None    # [s]

        self._interval = None    # [ms]
        self._speed = None    # [1=realtime]
        self._frames = None
        self._action = None

        self._math_utils = None

        self._name = None

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_depth(self):
        return self._depth

    def get_mount_point(self):
        return self._mount_point

    def get_start_pos(self):
        return self._start_pos

    def get_start_vel(self):
        return self._start_vel

    def get_magnets(self):
        return self._magnets

    def get_friction(self):
        return self._friction

    def get_disturbance(self):
        return self._disturbance

    def get_m(self):
        return self._m

    def get_g(self):
        return self._g

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

    def get_math_utils(self):
        return self._math_utils

    def get_name(self):
        return self._name


class BaseConfig:

    @staticmethod
    def _floor_position(radius, angle):
        x = radius * math.cos(angle * (math.pi / 180))
        y = radius * math.sin(angle * (math.pi / 180))
        pos = np.array([x, y, 0])
        return pos

    @staticmethod
    def _room_position_tp(mp, radius, theta, phi):

        x = radius * math.sin(theta) * math.cos(phi)
        y = radius * math.sin(theta) * math.sin(phi)
        z = radius * math.cos(theta)

        v = np.array([x, y, z])
        v[2] = -v[2]
        v = mp + v

        return v

    @staticmethod
    def _room_position_xy(mp, radius, x, y):
        phi = math.atan2(y, x)
        theta = math.asin(x/(radius*math.cos(phi)))
        z = radius * math.cos(theta)
        v = np.array([x, y, z])
        v[2] = -v[2]
        v = mp + v
        return v

    @staticmethod
    def _get_config():
        config = Config()

        config._m = 1
        config._g = 9.81

        config._dt = 0.01

        config._interval = 100
        config._speed = 1

        config._math_utils = MathUtilsVec()

        return config
