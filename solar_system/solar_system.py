
import numpy as np

from body import Body
from solar_system_definitions import *


class SolarSystemBody(Body):

    def __init__(self, name, m, r, color, pos, vel, order_nr, mean_distance):
        super().__init__(name, m, r, color, pos, vel)
        self._order_nr = order_nr
        self._mean_distance = mean_distance

    def get_order_nr(self):
        return self._order_nr

    def get_mean_distance(self):
        return self._mean_distance


class SolarSystemBodyFactory:

    @staticmethod
    def normalize_pos(value):
        # AU to m
        return value * 1.496 * pow(10, 11)

    @staticmethod
    def normalize_vel(value):
        # AU/day to m/s
        return value * 1.731 * pow(10, 6)

    @staticmethod
    def __create_body(body_dict, ic_dict):
        # position
        x = SolarSystemBodyFactory.normalize_pos(ic_dict[X])
        y = SolarSystemBodyFactory.normalize_pos(ic_dict[Y])
        z = SolarSystemBodyFactory.normalize_pos(ic_dict[Z])
        sp = np.array([x, y, z])
        # velicity
        vx = SolarSystemBodyFactory.normalize_vel(ic_dict[VX])
        vy = SolarSystemBodyFactory.normalize_vel(ic_dict[VY])
        vz = SolarSystemBodyFactory.normalize_vel(ic_dict[VZ])
        sv = np.array([vx, vy, vz])
        # body
        return SolarSystemBody(
            name=body_dict[NAME],
            m=body_dict[MASS],
            r=body_dict[RADIUS],
            color=body_dict[COLOR],
            pos=sp,
            vel=sv,
            order_nr=body_dict[ORDER_NR],
            mean_distance=SolarSystemBodyFactory.normalize_pos(body_dict[MEAN_DISTANCE])
        )

    @staticmethod
    def sun_and_planets():
        return [
            SolarSystemBodyFactory.__create_body(SUN, SUN_IC),
            SolarSystemBodyFactory.__create_body(MERCURY, MERCURY_IC),
            SolarSystemBodyFactory.__create_body(VENUS, VENUS_IC),
            SolarSystemBodyFactory.__create_body(EARTH, EARTH_IC),
            SolarSystemBodyFactory.__create_body(MARS, MARS_IC),
            SolarSystemBodyFactory.__create_body(JUPITER, JUPITER_IC),
            SolarSystemBodyFactory.__create_body(SATURN, SATURN_IC),
            SolarSystemBodyFactory.__create_body(URANUS, URANUS_IC),
            SolarSystemBodyFactory.__create_body(NEPTUNE, NEPTUNE_IC)
        ]

    @staticmethod
    def sun_earth_and_moon():
        return [
            SolarSystemBodyFactory.__create_body(SUN, SUN_IC),
            SolarSystemBodyFactory.__create_body(EARTH, EARTH_IC),
            SolarSystemBodyFactory.__create_body(MOON, MOON_IC)
        ]
