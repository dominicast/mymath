
import math

from enum import Enum


class Impl(Enum):
    ANGLE_INTEG = 1
    FORCE_INTEG = 2


class Action(Enum):
    SHOW = 1
    HTML = 2


class Config:

    def __init__(self):
        self._radius = None
        self._rho_max = None
        self._phi = None
        self._time_factor = None

        self._m = None
        self._g = None

        self._friction = None

        self._integ_dt = None    # [s]
        self._integ_count = None
        self._integ_freq = None   # [ms]

        self._impl = None

        self._action = None

        self._frames = None

        self._name = None

    def get_radius(self):
        return self._radius

    def get_rho_max(self):
        return self._rho_max

    def get_phi(self):
        return self._phi

    def get_time_factor(self):
        return self._time_factor

    def get_m(self):
        return self._m

    def get_g(self):
        return self._g

    def get_friction(self):
        return self._friction

    def get_integ_dt(self):
        return self._integ_dt

    def get_integ_count(self):
        return self._integ_count

    def get_integ_freq(self):
        return self._integ_freq

    def get_impl(self):
        return self._impl

    def get_action(self):
        return self._action

    def get_frames(self):
        return self._frames

    def get_name(self):
        return self._name


class BaseConfig:

    def _get_config(self, impl):
        config = Config()

        config._radius = 10
        config._rho_max = math.radians(40)
        config._phi = math.radians(40)
        config._time_factor = 1

        config._m = 1
        config._g = 9.81

        config._integ_dt = 0.01
        config._integ_count = 10
        config._integ_freq = 100

        config._impl = impl

        return config


class NoFrictionConfig(BaseConfig):

    def get_config(self, impl, action):
        config = super()._get_config(impl)

        config._friction = 0
        config._name = 'no_friction'

        config._action = action

        if config.get_action() == Action.HTML:
            config._frames = 64

        return config
