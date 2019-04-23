import math
import numpy as np

# Jorge Rodriguez (14.07.2016)
# Math for Game Developers - Spaceship Orbits (Semi-Implicit Euler)
# https://www.youtube.com/watch?v=kxWBXd7ujx0
#
# Jorge Rodriguez (21.07.2016)
# Math for Game Developers - Verlet Integration
# https://www.youtube.com/watch?v=AZ8IGOHsjBk
#
# Wikipedia
# Beeman's algorithm
# https://en.wikipedia.org/wiki/Beeman%27s_algorithm#Equation


class EulerBase:

    def __init__(self, eq, init_pos, init_vel):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

    def execute(self, dt, n_max, observer=None):

        n = 0
        t = 0

        pos = self._init_pos
        vel = self._init_vel

        while True:

            if not (observer is None):
                if observer.notify(pos, vel, t, n):
                    return

            acc = self._eq.f(pos=pos, vel=vel, t=t, n=n)

            vel_n = vel + dt * acc
            pos_n = pos + dt * self._chose_velocity(vel, vel_n)

            # --

            n += 1
            t += dt

            if n > n_max:
                return

            vel = vel_n
            pos = pos_n


class Euler(EulerBase):

    @staticmethod
    def _chose_velocity(vel, vel_n):
        return vel


class SIEuler(EulerBase):

    @staticmethod
    def _chose_velocity(vel, vel_n):
        return vel_n


class Verlet:

    def __init__(self, eq, init_pos, init_vel):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

    def execute(self, dt, n_max, observer=None):

        dt_rez=(1/dt)

        # --

        n = 0
        t = 0

        pos = self._init_pos
        vel = self._init_vel
        acc = self._eq.f(pos=pos, vel=vel, t=t, n=n)

        if not (observer is None):
            if observer.notify(pos, vel, t, n):
                return

        pos_n = pos + vel * dt + (1 / 2) * acc * math.pow(dt, 2)

        # --

        n += 1
        t += dt

        pos_p = pos
        pos = pos_n

        while True:

            vel = (pos - pos_p) * dt_rez
            acc = self._eq.f(pos=pos, vel=vel, t=t, n=n)

            if not (observer is None):
                if observer.notify(pos, vel, t, n):
                    return

            pos_n = 2 * pos - pos_p + acc * math.pow(dt, 2)

            # --

            n += 1
            t += dt

            if n > n_max:
                return

            pos_p = pos
            pos = pos_n


# class BeemanBTF:
#
#     def __init__( self, eq, init_pos, init_vel ):
#         self._eq = eq
#         self._init_pos = init_pos
#         self._init_vel = init_vel
#
#     def execute( self, h, n, observer=None ):
#
#         pos = self._init_pos
#         vel = self._init_vel
#
#         acc_p = np.array([0, 0])
#         acc = np.array([0, 0])
#         acc_n = np.array([0, 0])
#
#         t = 0
#         dt = h
#
#         if not (observer is None):
#             if observer.notify(pos, vel, t, 0):
#                 return
#
#         for i in range(1, n):
#
#             t += dt
#
#             pos = pos + vel * dt + math.pow( dt, 2 ) * ( (2/3) * acc - (1/6) * acc_p )
#
#             if not (observer is None):
#                 if observer.notify(pos, vel, t, i):
#                     return
#
#             acc_n = self._eq.f(pos=pos, vel=vel, t=t, n=i)
#
#             vel = vel + dt * ( (1/3) * acc_n + (5/6) * acc - (1/6) * acc_p )
#
#             tmp = acc_p
#             acc_p = acc
#             acc = acc_n
#             acc_n = tmp
