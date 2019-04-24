import math
import numpy as np


# Jorge Rodriguez (14.07.2016)
# Math for Game Developers - Spaceship Orbits (Semi-Implicit Euler)
# https://www.youtube.com/watch?v=kxWBXd7ujx0
class EulerBase:

    def __init__(self, eq, init_pos, init_vel):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

    def f(self, pos, vel, t, n, dt):
        return self._eq.f(pos=pos, vel=vel, t=t, n=n)

    def execute(self, dt, n_max, observer=None):

        n = 0
        t = 0

        pos = self._init_pos
        vel = self._init_vel

        while True:

            if not (observer is None):
                if observer.notify(pos, vel, t, n):
                    return

            acc = self.f(pos=pos, vel=vel, t=t, n=n, dt=dt)

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


# I am not sure if this is implemented correctly for for 2nd order ODE's
# as I use Midpoint method only for the integration of the velocity
# the results are not too bad but it could maybe implemented better
#
# Jorge Rodriguez (28.07.2016)
# Math for Game Developers - Midpoint Method
# https://www.youtube.com/watch?v=2hjoqAaH5kc
class Midpoint:

    def __init__(self, eq, init_pos, init_vel):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

    def f(self, pos, vel, t, n, dt):
        return self._eq.f(pos=pos, vel=vel, t=t, n=n)

    def execute(self, dt, n_max, observer=None):

        n = 0
        t = 0

        pos = self._init_pos
        vel = self._init_vel

        while True:

            if not (observer is None):
                if observer.notify(pos, vel, t, n):
                    return

            vel_mp = vel + (dt/2) * self._eq.f(pos=pos, vel=vel, t=t, n=n)
            vel_n = vel + dt * self._eq.f(pos=pos, vel=vel_mp, t=t+(dt/2), n=n)

            pos_n = pos + dt * vel_n

            # --

            n += 1
            t += dt

            if n > n_max:
                return

            vel = vel_n
            pos = pos_n


# Jorge Rodriguez (21.07.2016)
# Math for Game Developers - Verlet Integration
# https://www.youtube.com/watch?v=AZ8IGOHsjBk
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


# This is the algorithmy used by:
#
# beltoforion.de
# Introducing the Magnetic Pendulum
# https://beltoforion.de/article.php?a=magnetic_pendulum&hl=en
#
# I am not sure how complete or good it is
# Probably it would be better to use is with 'Predictor-corrector modifications'
#
# Wikipedia
# Beeman's algorithm
# https://en.wikipedia.org/wiki/Beeman%27s_algorithm#Equation
class Beeman:

    def __init__(self, eq, init_pos, init_vel):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

    def execute(self, dt, n_max, observer=None):

        acc_p = np.array([0, 0])
        acc = np.array([0, 0])

        pos = self._init_pos
        vel = self._init_vel

        n = 0
        t = 0

        if not (observer is None):
            if observer.notify(pos, vel, t, n):
                return

        while True:

            n += 1
            t += dt

            if n > n_max:
                return

            pos = pos + vel * dt + math.pow( dt, 2 ) * ( (2/3) * acc - (1/6) * acc_p )

            if not (observer is None):
                if observer.notify(pos, vel, t, n):
                    return

            acc_n = self._eq.f(pos=pos, vel=vel, t=t, n=n)

            vel = vel + dt * ( (1/3) * acc_n + (5/6) * acc - (1/6) * acc_p )

            acc_p = acc
            acc = acc_n
