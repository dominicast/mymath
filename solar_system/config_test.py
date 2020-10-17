
import numpy as np
from body import *


class BodiesFactory:

    @staticmethod
    def create_u():
        mass = 50
        radius = 1
        position = np.array([[0., 0., 0.]])
        velocity = np.array([[0., 0., 0.]])
        size = 1
        color = (1., 0., 0.)
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size)

    @staticmethod
    def create_v():
        mass = 1
        radius = 1
        position = np.array([[10., 10., 10.]])
        velocity = np.array([[0., 1., 0.]])
        # size = radius
        size = 1
        color = (0., 0., 1.)
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size)

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

    def get_bodies(self):
        return self._bodies

    def get_G(self):
        return self._G

    def get_speed(self):
        return self._speed

    def get_dt(self):
        return self._dt
