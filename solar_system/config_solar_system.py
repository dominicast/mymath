
import math
from solar_system import *


class Displacer:

    def __init__(self, fact):
        self._fact = fact

    def map(self, value):
        result = (value*self._fact)
        return result


class Scaler:

    @staticmethod
    def __calc_distance_scale(index, mean_distance):
        if index == 0:
            index = (1/100)
        return index * 100 * (1 / mean_distance)

    @staticmethod
    def calc_size(radius, mass):
        return 14 * math.log(radius / pow(10, 6), math.e)

    @staticmethod
    def create_displacer(mean_distance, body_index):
        if body_index == 0:
            mean_distance = pow(10, 9)
        distance_scale = Scaler.__calc_distance_scale(body_index, mean_distance)
        return Displacer(distance_scale)


class Config:

    def __init__(self):
        self._bodies = SolarSystemBodyFactory.sun_and_planets(Scaler())
        self._G = 6.6743*pow(10, -11)
        self._speed = 1000000
        # self._speed = 56560
        self._dt = 0.001
        self._azimuth = 45
        self._elevation = 66
        self._distance = 2000
        self._show_names = True

    def get_bodies(self):
        return self._bodies

    def get_G(self):
        return self._G

    def get_speed(self):
        return self._speed

    def get_dt(self):
        return self._dt

    def get_azimuth(self):
        return self._azimuth

    def get_elevation(self):
        return self._elevation

    def get_distance(self):
        return self._distance

    def show_names(self):
        return self._show_names
