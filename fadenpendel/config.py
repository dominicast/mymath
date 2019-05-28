
import math

from enum import Enum

class Impl(Enum):
    ANGLE = 1
    FORCE = 2


class Config:

    def __init__(self):
        self.radius = 10
        self.rho_max = math.radians(40)
        self.time_factor = 1

        self.integ_dt = 0.01    # [s]
        self.integ_count = 10
        self.integ_freq = 100   # [ms]

        self.impl = Impl.FORCE

    def get_radius(self):
        return self.radius

    def get_rho_max(self):
        return self.rho_max

    def get_time_factor(self):
        return self.time_factor

    def get_integ_dt(self):
        return self.integ_dt

    def get_integ_count(self):
        return self.integ_count

    def get_integ_freq(self):
        return self.integ_freq

    def get_impl(self):
        return self.impl
