
import numpy as np

from body import Body, SimulationBody
from solar_system_definitions import *


class SolarSystemBody(Body):

    def __init__(self, name, m, r, color, order_nr, mean_distance):
        super().__init__(name, m, r, color)
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
    def parse_ics(ic_dict):
        # position
        x = SolarSystemBodyFactory.normalize_pos(ic_dict[X])
        y = SolarSystemBodyFactory.normalize_pos(ic_dict[Y])
        z = SolarSystemBodyFactory.normalize_pos(ic_dict[Z])
        sp = np.array([[x, y, z]])
        # velicity
        vx = SolarSystemBodyFactory.normalize_vel(ic_dict[VX])
        vy = SolarSystemBodyFactory.normalize_vel(ic_dict[VY])
        vz = SolarSystemBodyFactory.normalize_vel(ic_dict[VZ])
        sv = np.array([[vx, vy, vz]])
        return sp, sv

    @staticmethod
    def parse_body(body_dict):
        return SolarSystemBody(
            name=body_dict[NAME],
            m=body_dict[MASS],
            r=body_dict[RADIUS],
            color=body_dict[COLOR],
            order_nr=body_dict[ORDER_NR],
            mean_distance=SolarSystemBodyFactory.normalize_pos(body_dict[MEAN_DISTANCE])
        )

    @staticmethod
    def __create_body_2(body, sp, sv, scaler):
        projector = None if scaler is None else scaler.create_projector(body)
        size = 2*body.get_r() if scaler is None else scaler.calc_size(body)
        return SimulationBody(
            name=body.get_name(),
            m=body.get_m(),
            r=body.get_r(),
            pos=sp,
            vel=sv,
            color=body.get_color(),
            size=size,
            projector=projector
        )

    @staticmethod
    def __create_body(body_dict, ic_dict, scaler):
        body = SolarSystemBodyFactory.parse_body(body_dict)
        sp, sv = SolarSystemBodyFactory.parse_ics(ic_dict)
        return SolarSystemBodyFactory.__create_body_2(
            body=body,
            sp=sp,
            sv=sv,
            scaler=scaler
        )

    @staticmethod
    def sun_and_planets(scaler=None):
        return [
            SolarSystemBodyFactory.__create_body(SUN, SUN_IC, scaler),
            SolarSystemBodyFactory.__create_body(MERCURY, MERCURY_IC, scaler),
            SolarSystemBodyFactory.__create_body(VENUS, VENUS_IC, scaler),
            SolarSystemBodyFactory.__create_body(EARTH, EARTH_IC, scaler),
            SolarSystemBodyFactory.__create_body(MARS, MARS_IC, scaler),
            SolarSystemBodyFactory.__create_body(JUPITER, JUPITER_IC, scaler),
            SolarSystemBodyFactory.__create_body(SATURN, SATURN_IC, scaler),
            SolarSystemBodyFactory.__create_body(URANUS, URANUS_IC, scaler),
            SolarSystemBodyFactory.__create_body(NEPTUNE, NEPTUNE_IC, scaler)
        ]

    @staticmethod
    def sun_earth_and_moon(scaler=None):
        return [
            SolarSystemBodyFactory.__create_body(SUN, SUN_IC, scaler),
            SolarSystemBodyFactory.__create_body(EARTH, EARTH_IC, scaler),
            SolarSystemBodyFactory.__create_body(MOON, MOON_IC, scaler)
        ]
