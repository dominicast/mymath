
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
        self._radius = 10
        self._rho_max = math.radians(40)
        self._phi = math.radians(40)
        self._time_factor = 1

        self._m = 1
        self._g = 9.81

        self._friction = 0
        #self._friction = 0.01

        self._integ_dt = 0.01    # [s]
        self._integ_count = 10
        self._integ_freq = 100   # [ms]

        self._impl = Impl.FORCE_INTEG
        #self._impl = Impl.ANGLE_INTEG

        self._action = Action.HTML
        #self._action = Action.SHOW

        self._frames = 64
        #self._frames = None

        self._name = 'no_friction'

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