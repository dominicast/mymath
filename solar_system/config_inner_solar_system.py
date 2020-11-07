
from solar_system import *
from solar_system_definitions import SUN_NAME


class Projector:

    def __init__(self, bodies):
        for body in bodies:
            body.proj_size = self.__calc_size(body)
            if body.get_name() == EARTH_NAME:
                self._earth = body

    @staticmethod
    def __calc_size(body):
        radius = body.get_r()
        if body.get_name() == SUN_NAME:
            return radius / pow(10, 6)
        else:
            return (2 * radius) / pow(10, 5)

    def get_pos(self, body):
        if body.get_name() != MOON_NAME:
            return body.get_pos() * pow(10, -8)
        v_e_m = body.get_pos() - self._earth.get_pos()
        return pow(10, -8) * self._earth.get_pos() + 3 * pow(10, -7) * v_e_m

    @staticmethod
    def get_size(body):
        return body.proj_size


class Config:

    def __init__(self):
        self._bodies = SolarSystemBodyFactory.all()
        self._G = 6.6743*pow(10, -11)
        # self._speed = 100
        # self._speed = 56560
        self._speed = 1000000
        self._dt = 0.001
        self._azimuth = 0
        self._elevation = 60
        self._focalpoint = (600., 0., 0.)
        self._distance = 5000
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

    def get_focalpoint(self):
        return self._focalpoint

    def get_distance(self):
        return self._distance

    def show_names(self):
        return self._show_names
