
import numpy as np
from body import *


class PositionMapper:

    @staticmethod
    def map(value):
        return value / 1000


class BodiesFactory:

    @staticmethod
    def create_sun():
        mass = 1.98892*pow(10,30)
        radius = 6.96342*pow(10,8)
        position = np.array([[0., 0., 0.]])
        velocity = np.array([[0., 0., 0.]])
        size = (6.96342*pow(10,8)/100)
        color = (1., 0., 0.)
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size, pos_mapper=PositionMapper())

    @staticmethod
    def create_earth():
        mass = 5.9722*pow(10,24)
        radius = 6.371*pow(10,6)
        distance = 1.5*pow(10,11)
        velocity = 30000
        position = np.array([[distance, 0., 0.]])
        velocity = np.array([[0., 0., velocity]])
        size = (6.96342*pow(10,8)/100)
        color = (0., 0., 1.)
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size, pos_mapper=PositionMapper())

    @staticmethod
    def create_bodies():

        sun = BodiesFactory.create_sun()
        earth = BodiesFactory.create_earth()

        bodies = [sun, earth]

        i = 0
        for body in bodies:
            body.set_index(i)
            i = i + 1

        return bodies


class Config:

    def __init__(self):
        body_factory = BodiesFactory()
        self._bodies = body_factory.create_bodies()
        self._G = 6.6743*pow(10,-11)
        self._speed = 1000000
        self._dt = 0.001

    def get_bodies(self):
        return self._bodies

    def get_G(self):
        return self._G

    def get_speed(self):
        return self._speed

    def get_dt(self):
        return self._dt
