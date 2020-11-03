
import numpy as np
from body import Body


class BodiesFactory:

    @staticmethod
    def create_u():
        mass = 1
        radius = 1
        position = np.array([1., 0., 0.])
        velocity = np.array([0., 0., 1.])
        color = (1., 0., 0.)
        return Body(name="u", m=mass, r=radius, color=color, pos=position, vel=velocity)

    @staticmethod
    def create_v():
        mass = 1
        radius = 1
        position = np.array([-1., 0., 0.])
        velocity = np.array([0., 0., -1.])
        color = (0., 0., 1.)
        return Body(name="v", m=mass, r=radius, color=color, pos=position, vel=velocity)

    @staticmethod
    def create_bodies():
        u = BodiesFactory.create_u()
        v = BodiesFactory.create_v()
        return [u, v]


class Projector:

    @staticmethod
    def get_pos(body):
        return body.get_pos()

    @staticmethod
    def get_size(body):
        return body.get_r()


class Config:

    def __init__(self):
        self._bodies = BodiesFactory.create_bodies()
        self._G = 2.5
        self._speed = 6
        self._dt = 0.001
        self._azimuth = 270
        self._elevation = 20
        self._distance = 40
        self._show_names = True

    @staticmethod
    def create_projector():
        return Projector()

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
