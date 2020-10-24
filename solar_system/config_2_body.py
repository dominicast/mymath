
import numpy as np
from body import SimulationBody


class BodiesFactory:

    @staticmethod
    def create_u():
        mass = 1
        radius = 1
        position = np.array([[1., 1., 1.]])
        velocity = np.array([[0., 0., 0.]])
        size = 1
        color = (1., 0., 0.)
        return SimulationBody(name="u", m=mass, r=radius, sp=position, sv=velocity, color=color, size=size)

    @staticmethod
    def create_v():
        mass = 1
        radius = 1
        position = np.array([[0., 0., 0.]])
        velocity = np.array([[0., 1., 0.]])
        #size = radius
        size = 1
        color = (0., 0., 1.)
        return SimulationBody(name="v", m=mass, r=radius, sp=position, sv=velocity, color=color, size=size)

    @staticmethod
    def create_bodies():

        u = BodiesFactory.create_u()
        v = BodiesFactory.create_v()

        bodies = [u, v]

        i = 0
        for body in bodies:
            body.set_index(i)
            i = i + 1

        return bodies


class Config:

    def __init__(self):
        body_factory = BodiesFactory()
        self._bodies = body_factory.create_bodies()
        self._G = 1
        self._speed = 3
        self._dt = 0.001
        self._azimuth = 0
        self._elevation = 90
        self._distance = 80

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
