
import math
from solar_system import *


class Projector:

    def __init__(self, bodies):
        for body in bodies:
            body.proj_size = self.__calc_size(body)
            body.proj_factor = self.__calc_factor(body)

    @staticmethod
    def __calc_size(body):
        radius = body.get_r()
        return 14 * math.log(radius / pow(10, 6), math.e)

    @staticmethod
    def __calc_factor(body):
        mean_distance = body.get_mean_distance()
        order_nr = body.get_order_nr()
        if order_nr == 0:
            mean_distance = pow(10, 9)
            order_nr = (1 / 100)
        return order_nr * 100 * (1 / mean_distance)

    @staticmethod
    def get_pos(body):
        return body.get_pos() * body.proj_factor

    @staticmethod
    def get_size(body):
        return body.proj_size


class Config:

    def __init__(self):
        self._bodies = SolarSystemBodyFactory.sun_and_planets()
        self._G = 6.6743*pow(10, -11)
        self._speed = 1000000
        # self._speed = 56560
        self._dt = 0.001
        self._azimuth = 45
        self._elevation = 66
        self._distance = 2000
        self._show_names = True

    def create_projector(self):
        return Projector(self._bodies)

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
