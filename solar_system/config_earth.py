
import math
from solar_system import *


class Projector:

    def __init__(self, fact):
        self._fact = fact

    def project(self, value, bodies):
        return value * 0.001


class Scaler:

    @staticmethod
    def __calc_distance_scale(order_nr, mean_distance):
        if order_nr == 0:
            order_nr = (1/100)
        return order_nr * 100 * (1 / mean_distance)

    @staticmethod
    def calc_size(body):
        order_nr = body.get_order_nr()
        radius = body.get_r()
        if order_nr == 0:
            return radius / 10
        else:
            return 2 * radius

    @staticmethod
    def create_projector(body):
        mean_distance = body.get_mean_distance()
        order_nr = body.get_order_nr()
        if order_nr == 0:
            mean_distance = pow(10, 9)
        distance_scale = Scaler.__calc_distance_scale(order_nr, mean_distance)
        return Projector(0.00001)


class Config:

    def __init__(self):
        self._bodies = SolarSystemBodyFactory.sun_earth_and_moon(Scaler())
        self._G = 6.6743*pow(10, -11)
        # self._speed = 100
        # self._speed = 56560
        self._speed = 1000000
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
