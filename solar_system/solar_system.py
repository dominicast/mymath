
import numpy as np

from body import SimulationBody
from solar_system_definitions import *


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
    def __create_body_2(body, sp, sv, scaler):

        name = body[NAME]
        mass = body[MASS]
        radius = body[RADIUS]
        color = body[COLOR]
        order_nr = body[ORDER_NR]
        mean_distance = SolarSystemBodyFactory.normalize_pos(body[MEAN_DISTANCE])

        displacer = None if scaler is None else scaler.create_displacer(mean_distance, order_nr)
        size = 2*radius if scaler is None else scaler.calc_size(radius, mass)

        return SimulationBody(
            name=name,
            m=mass,
            r=radius,
            sp=sp,
            sv=sv,
            color=color,
            size=size,
            displacer=displacer
        )

    @staticmethod
    def __create_body(body, ics, scaler):

        # initial position
        x = SolarSystemBodyFactory.normalize_pos(ics[X])
        y = SolarSystemBodyFactory.normalize_pos(ics[Y])
        z = SolarSystemBodyFactory.normalize_pos(ics[Z])
        sp = np.array([[x, y, z]])

        # initial velocity
        vx = SolarSystemBodyFactory.normalize_vel(ics[VX])
        vy = SolarSystemBodyFactory.normalize_vel(ics[VY])
        vz = SolarSystemBodyFactory.normalize_vel(ics[VZ])
        sv = np.array([[vx, vy, vz]])

        return SolarSystemBodyFactory.__create_body_2(
            body=body,
            sp=sp,
            sv=sv,
            scaler=scaler
        )

    @staticmethod
    def sun_and_planets(scaler=None):

        bodies = [
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

        i = 0
        for body in bodies:
            body.set_index(i)
            i = i + 1

        return bodies
