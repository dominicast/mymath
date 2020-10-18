
import numpy as np
from body import *


class PositionMapper:

    @staticmethod
    def map(value):
        return value / 1000


class BodiesFactory:

    @staticmethod
    def normalize_pos(value):
        # AU to m
        return value * 1.496 * pow(10, 11)

    @staticmethod
    def normalize_vel(value):
        # AU/day to m/s
        return value * 1.731 * pow(10, 6)

    @staticmethod
    def create_sun():
        mass = 1.9885*pow(10, 30)
        radius = 6.957*pow(10, 8)
        # position
        position = np.array([[0., 0., 0.]])
        # velocity
        velocity = np.array([[0., 0., 0.]])
        # view
        size = (6.96342*pow(10, 8)/100)
        color = (1., 0., 0.)
        # body
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size, pos_mapper=PositionMapper())

    @staticmethod
    def create_mercury():
        mass = 3.302*pow(10, 23)
        radius = 2.44*pow(10, 6)
        # position
        x = BodiesFactory.normalize_pos(2.699256202625721 * pow(10, -1))
        y = BodiesFactory.normalize_pos(-2.945510912763388 * pow(10, -1))
        z = BodiesFactory.normalize_pos(-3.696675812633399 * pow(10, -4))
        position = np.array([[x, y, z]])
        # velocity
        vx = BodiesFactory.normalize_vel(1.561896404958095 * pow(10, -2))
        vy = BodiesFactory.normalize_vel(2.169157526816811 * pow(10, -2))
        vz = BodiesFactory.normalize_vel(1.551833430476102 * pow(10, -3))
        velocity = np.array([[vx, vy, vz]])
        # view
        size = (6.96342*pow(10, 8)/100)
        color = (0., 0., 1.)
        # body
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size, pos_mapper=PositionMapper())

    @staticmethod
    def create_venus():
        mass = 4.8685*pow(10, 24)
        radius = 6.05184*pow(10, 6)
        # position
        x = BodiesFactory.normalize_pos(5.464852488455190 * pow(10, -1))
        y = BodiesFactory.normalize_pos(-4.783861666843854 * pow(10, -1))
        z = BodiesFactory.normalize_pos(4.798888564017594 * pow(10, -2))
        position = np.array([[x, y, z]])
        # velocity
        vx = BodiesFactory.normalize_vel(1.318627597778329 * pow(10, -2))
        vy = BodiesFactory.normalize_vel(1.516700055825804 * pow(10, -2))
        vz = BodiesFactory.normalize_vel(2.662965477224826 * pow(10, -4))
        velocity = np.array([[vx, vy, vz]])
        # view
        size = (6.96342*pow(10, 8)/100)
        color = (0., 0., 1.)
        # body
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size, pos_mapper=PositionMapper())

    @staticmethod
    def create_earth():
        mass = 5.97219*pow(10, 24)
        radius = 6.37101*pow(10, 6)
        # position
        x = BodiesFactory.normalize_pos(9.770505872741465 * pow(10, -1))
        y = BodiesFactory.normalize_pos(1.690040669781609 * pow(10, -1))
        z = BodiesFactory.normalize_pos(9.843601704544269 * pow(10, -2))
        position = np.array([[x, y, z]])
        # velocity
        vx = BodiesFactory.normalize_vel(-3.077197091901566 * pow(10, -3))
        vy = BodiesFactory.normalize_vel(1.692320172129821 * pow(10, -2))
        vz = BodiesFactory.normalize_vel(-1.383397601779740 * pow(10, -3))
        velocity = np.array([[vx, vy, vz]])
        # view
        size = (6.96342*pow(10, 8)/100)
        color = (0., 0., 1.)
        # body
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size, pos_mapper=PositionMapper())

    @staticmethod
    def create_moon():
        mass = 7.349*pow(10, 22)
        radius = 1.73753*pow(10, 6)
        # position
        x = BodiesFactory.normalize_pos(9.795481265482870 * pow(10, -1))
        y = BodiesFactory.normalize_pos(1.687280949525631 * pow(10, -1))
        z = BodiesFactory.normalize_pos(9.884749180681386 * pow(10, -2))
        position = np.array([[x, y, z]])
        # velocity
        vx = BodiesFactory.normalize_vel(-2.977622074551740 * pow(10, -3))
        vy = BodiesFactory.normalize_vel(1.750905810358991 * pow(10, -2))
        vz = BodiesFactory.normalize_vel(-1.455473815404281 * pow(10, -3))
        velocity = np.array([[vx, vy, vz]])
        # view
        size = (6.96342*pow(10, 8)/100)
        color = (1., 0., 0.)
        # body
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size, pos_mapper=PositionMapper())

    @staticmethod
    def create_mars():
        mass = 6.4171*pow(10, 23)
        radius = 3.38992*pow(10, 6)
        # position
        x = BodiesFactory.normalize_pos(-4.839729488908665 * pow(10, -1))
        y = BodiesFactory.normalize_pos(1.560630802450471 * pow(10, 0))
        z = BodiesFactory.normalize_pos(-9.913374596063972 * pow(10, -2))
        position = np.array([[x, y, z]])
        # velocity
        vx = BodiesFactory.normalize_vel(-1.249711683427429 * pow(10, -2))
        vy = BodiesFactory.normalize_vel(-3.172037129830012 * pow(10, -3))
        vz = BodiesFactory.normalize_vel(-1.047799161775436 * pow(10, -3))
        velocity = np.array([[vx, vy, vz]])
        # view
        size = (6.96342*pow(10, 8)/100)
        color = (0., 1., 0.)
        # body
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size, pos_mapper=PositionMapper())

    @staticmethod
    def create_jupiter():
        mass = 1.89813*pow(10, 27)
        radius = 6.9911*pow(10, 7)
        # position
        x = BodiesFactory.normalize_pos(5.653696041446783 * pow(10, -1))
        y = BodiesFactory.normalize_pos(5.126945373315730 * pow(10, 0))
        z = BodiesFactory.normalize_pos(-2.563779438429464 * pow(10, -1))
        position = np.array([[x, y, z]])
        # velocity
        vx = BodiesFactory.normalize_vel(-7.477161414122874 * pow(10, -3))
        vy = BodiesFactory.normalize_vel(1.157735522887552 * pow(10, -3))
        vz = BodiesFactory.normalize_vel(-7.304406745079823 * pow(10, -4))
        velocity = np.array([[vx, vy, vz]])
        # view
        size = (6.96342*pow(10, 8)/100)
        color = (0., 1., 0.)
        # body
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size, pos_mapper=PositionMapper())

    @staticmethod
    def create_saturn():
        mass = 5.6834*pow(10, 26)
        radius = 5.8232*pow(10, 7)
        # position
        x = BodiesFactory.normalize_pos(-8.646714279106760 * pow(10, 0))
        y = BodiesFactory.normalize_pos(-4.738275608763417 * pow(10, 0))
        z = BodiesFactory.normalize_pos(-2.658804447914820 * pow(10, -1))
        position = np.array([[x, y, z]])
        # velocity
        vx = BodiesFactory.normalize_vel(2.359453009042619 * pow(10, -3))
        vy = BodiesFactory.normalize_vel(-4.813470722521699 * pow(10, -3))
        vz = BodiesFactory.normalize_vel(4.882764918036705 * pow(10, -4))
        velocity = np.array([[vx, vy, vz]])
        # view
        size = (6.96342*pow(10, 8)/100)
        color = (0., 1., 0.)
        # body
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size, pos_mapper=PositionMapper())

    @staticmethod
    def create_uranus():
        mass = 8.6813*pow(10, 25)
        radius = 2.5362*pow(10, 7)
        # position
        x = BodiesFactory.normalize_pos(1.988385163968572 * pow(10, 1))
        y = BodiesFactory.normalize_pos(-1.405926882792088 * pow(10, 0))
        z = BodiesFactory.normalize_pos(2.057920386344378 * pow(10, 0))
        position = np.array([[x, y, z]])
        # velocity
        vx = BodiesFactory.normalize_vel(2.155405725825843 * pow(10, -4))
        vy = BodiesFactory.normalize_vel(3.747819746273274 * pow(10, -3))
        vz = BodiesFactory.normalize_vel(-1.826727345802505 * pow(10, -4))
        velocity = np.array([[vx, vy, vz]])
        # view
        size = (6.96342*pow(10, 8)/100)
        color = (0., 1., 0.)
        # body
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size, pos_mapper=PositionMapper())

    @staticmethod
    def create_neptune():
        mass = 1.024*pow(10, 26)
        radius = 2.4624*pow(10, 7)
        # position
        x = BodiesFactory.normalize_pos(2.259965604627899 * pow(10, 1))
        y = BodiesFactory.normalize_pos(-1.941340140795343 * pow(10, 1))
        z = BodiesFactory.normalize_pos(3.357236604763358 * pow(10, 0))
        position = np.array([[x, y, z]])
        # velocity
        vx = BodiesFactory.normalize_vel(2.026226391500671 * pow(10, -3))
        vy = BodiesFactory.normalize_vel(2.404346714025546 * pow(10, -3))
        vz = BodiesFactory.normalize_vel(-1.197451013633338 * pow(10, -5))
        velocity = np.array([[vx, vy, vz]])
        # view
        size = (6.96342*pow(10, 8)/100)
        color = (0., 1., 0.)
        # body
        return VisibleBody(m=mass, r=radius, sp=position, sv=velocity, color=color, size=size, pos_mapper=PositionMapper())

    @staticmethod
    def create_bodies():

        # positin at 2013-Oct-17 16:00:00.0000

        sun = BodiesFactory.create_sun()
        mercury = BodiesFactory.create_mercury()
        venus = BodiesFactory.create_venus()
        earth = BodiesFactory.create_earth()
        moon = BodiesFactory.create_moon()
        mars = BodiesFactory.create_mars()
        jupiter = BodiesFactory.create_jupiter()
        saturn = BodiesFactory.create_saturn()
        uranus = BodiesFactory.create_uranus()
        neptune = BodiesFactory.create_neptune()

        bodies = [sun, mercury, venus, earth, moon, mars]
        # bodies = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

        i = 0
        for body in bodies:
            body.set_index(i)
            i = i + 1

        return bodies


class Config:

    def __init__(self):
        body_factory = BodiesFactory()
        self._bodies = body_factory.create_bodies()
        self._G = 6.6743*pow(10, -11)
        #self._speed = 1000000
        self._speed = 56560
        self._dt = 0.001

    def get_bodies(self):
        return self._bodies

    def get_G(self):
        return self._G

    def get_speed(self):
        return self._speed

    def get_dt(self):
        return self._dt
