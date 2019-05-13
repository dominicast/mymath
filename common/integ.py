import math
import numpy as np


# Jorge Rodriguez (14.07.2016)
# Math for Game Developers - Spaceship Orbits (Semi-Implicit Euler)
# https://www.youtube.com/watch?v=kxWBXd7ujx0
class EulerBase:

    def __init__(self, eq, init_pos, init_vel, observer=None):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

        self._observer = observer

        self._ff_n = None
        self._ff_t = None
        self._ff_pos = None
        self._ff_vel = None

    def _continuing(self):
        if self._ff_n is None:
            return False
        if self._ff_t is None:
            return False
        if self._ff_pos is None:
            return False
        if self._ff_vel is None:
            return False
        return True

    def _notify(self, pos, vel, t, n):
        if self._observer is None:
            return False
        if self._observer.notify(pos, vel, t, n):
            return True
        else:
            return False

    def execute(self, dt, count):

        if not self._continuing():
            n = 0
            t = 0
            pos = self._init_pos
            vel = self._init_vel
        else:
            n = self._ff_n
            t = self._ff_t
            pos = self._ff_pos
            vel = self._ff_vel

        n_max = None if count is None else n + count

        while True:

            if self._notify(pos, vel, t, n):
                break

            acc = self._eq.f(pos=pos, vel=vel, t=t)

            vel_n = vel + dt * acc

            #if n % 100 == 0:
            #    print( '('+repr(pos[0])+','+repr(pos[1])+','+repr(pos[2])+') - ('+repr(vel[0])+','+repr(vel[1])+','+repr(vel[2])+')' )

            pos_n = pos + dt * self._chose_velocity(vel, vel_n)

            # --

            n += 1
            t += dt
            vel = vel_n
            pos = pos_n

            if n_max is not None and n > n_max:
                break

        self._ff_n = n
        self._ff_t = t
        self._ff_pos = pos
        self._ff_vel = vel

        return pos, vel


class Euler(EulerBase):

    @staticmethod
    def _chose_velocity(vel, vel_n):
        return vel


class SIEuler(EulerBase):

    @staticmethod
    def _chose_velocity(vel, vel_n):
        return vel_n


# I am not sure if this is implemented correctly for for 2nd order ODE's
# as I use Midpoint method only for the integration of the velocity
# the results are not too bad but it could maybe implemented better
#
# Jorge Rodriguez (28.07.2016)
# Math for Game Developers - Midpoint Method
# https://www.youtube.com/watch?v=2hjoqAaH5kc
class Midpoint:

    def __init__(self, eq, init_pos, init_vel, observer=None):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

        self._observer = observer

        self._ff_n = None
        self._ff_t = None
        self._ff_pos = None
        self._ff_vel = None

    def _continuing(self):
        if self._ff_n is None:
            return False
        if self._ff_t is None:
            return False
        if self._ff_pos is None:
            return False
        if self._ff_vel is None:
            return False
        return True

    def _notify(self, pos, vel, t, n):
        if self._observer is None:
            return False
        if self._observer.notify(pos, vel, t, n):
            return True
        else:
            return False

    def execute(self, dt, count):

        if not self._continuing():
            n = 0
            t = 0
            pos = self._init_pos
            vel = self._init_vel
        else:
            n = self._ff_n
            t = self._ff_t
            pos = self._ff_pos
            vel = self._ff_vel

        n_max = None if count is None else n + count

        while True:

            if self._notify(pos, vel, t, n):
                break

            vel_mp = vel + (dt/2) * self._eq.f(pos=pos, vel=vel, t=t)
            vel_n = vel + dt * self._eq.f(pos=pos, vel=vel_mp, t=t+(dt/2))

            pos_n = pos + dt * vel_n

            # --

            n += 1
            t += dt

            vel = vel_n
            pos = pos_n

            if n_max is not None and n > n_max:
                break

        self._ff_n = n
        self._ff_t = t
        self._ff_pos = pos
        self._ff_vel = vel

        return pos, vel


# Jorge Rodriguez (21.07.2016)
# Math for Game Developers - Verlet Integration
# https://www.youtube.com/watch?v=AZ8IGOHsjBk
class Verlet:

    def __init__(self, eq, init_pos, init_vel, observer=None):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

        self._observer = observer

        self._ff_n = None
        self._ff_t = None
        self._ff_pos = None
        self._ff_pos_p = None

    def _continuing(self):
        if self._ff_n is None:
            return False
        if self._ff_t is None:
            return False
        if self._ff_pos is None:
            return False
        if self._ff_pos_p is None:
            return False
        return True

    def _notify(self, pos, vel, t, n):
        if self._observer is None:
            return False
        if self._observer.notify(pos, vel, t, n):
            return True
        else:
            return False

    def execute(self, dt, count):

        dt_rez=(1/dt)

        if not self._continuing():

            # --

            n = 0
            t = 0

            pos = self._init_pos
            vel = self._init_vel
            acc = self._eq.f(pos=pos, vel=vel, t=t)

            if self._notify(pos, vel, t, n):
                return

            pos_n = pos + vel * dt + (1 / 2) * acc * math.pow(dt, 2)

            # --

            n += 1
            t += dt

            pos_p = pos
            pos = pos_n

        else:

            n = self._ff_n
            t = self._ff_t
            pos = self._ff_pos
            pos_p = self._ff_pos_p

        n_max = None if count is None else n + count

        while True:

            vel = (pos - pos_p) * dt_rez
            acc = self._eq.f(pos=pos, vel=vel, t=t)

            if self._notify(pos, vel, t, n):
                break

            pos_n = 2 * pos - pos_p + acc * math.pow(dt, 2)

            # --

            n += 1
            t += dt

            pos_p = pos
            pos = pos_n

            if n_max is not None and n > n_max:
                break

        self._ff_n = n
        self._ff_t = t
        self._ff_pos = pos
        self._ff_pos_p = pos_p

        return pos, vel


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

    def __init__(self, eq, init_pos, init_vel, observer=None):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

        self._observer = observer

        self._ff_n = None
        self._ff_t = None
        self._ff_pos = None
        self._ff_vel = None
        self._ff_acc = None
        self._ff_acc_p = None

    def _continuing(self):
        if self._ff_n is None:
            return False
        if self._ff_t is None:
            return False
        if self._ff_pos is None:
            return False
        if self._ff_vel is None:
            return False
        if self._ff_acc is None:
            return False
        if self._ff_acc_p is None:
            return False
        return True

    def _notify(self, pos, vel, t, n):
        if self._observer is None:
            return False
        if self._observer.notify(pos, vel, t, n):
            return True
        else:
            return False

    def execute(self, dt, count):

        if not self._continuing():

            try :
                acc_p = np.zeros(self._init_pos.size)
                acc = np.array(self._init_pos.size)
            except AttributeError:
                acc_p = 0
                acc = 0

            pos = self._init_pos
            vel = self._init_vel

            n = 0
            t = 0

        else:

            acc_p = self._ff_acc_p
            acc = self._ff_acc

            pos = self._ff_pos
            vel = self._ff_vel

            n = self._ff_n
            t = self._ff_t

        n_max = None if count is None else n + count

        if self._notify(pos, vel, t, n):
            return

        while True:

            n += 1
            t += dt

            if n_max is not None and n > n_max:
                break

            pos = pos + vel * dt + math.pow( dt, 2 ) * ( (2/3) * acc - (1/6) * acc_p )

            if self._notify(pos, vel, t, n):
                break

            acc_n = self._eq.f(pos=pos, vel=vel, t=t)

            vel = vel + dt * ( (1/3) * acc_n + (5/6) * acc - (1/6) * acc_p )

            acc_p = acc
            acc = acc_n

        self._ff_n = n
        self._ff_t = t
        self._ff_pos = pos
        self._ff_vel = vel
        self._ff_acc = acc
        self._ff_acc_p = acc_p

        return pos, vel


# Jorge Rodriguez (04.08.2016)
# Math for Game Developers - Runge-Kutta Order 4
# https://www.youtube.com/watch?v=hGCP6I2WisM
#
# Aleksandr Spiridonov (29.04.2011)
# Runge Kutta 4th order method for ODE2
# https://www.youtube.com/watch?v=smfX0Jt_f0I
class RungeKutta4th:

    def __init__(self, eq, init_pos, init_vel, observer=None):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

        self._observer = observer

        self._ff_n = None
        self._ff_t = None
        self._ff_pos = None
        self._ff_vel = None

    def _continuing(self):
        if self._ff_n is None:
            return False
        if self._ff_t is None:
            return False
        if self._ff_pos is None:
            return False
        if self._ff_vel is None:
            return False
        return True

    def _notify(self, pos, vel, t, n):
        if self._observer is None:
            return False
        if self._observer.notify(pos, vel, t, n):
            return True
        else:
            return False

    def execute(self, dt, count):

        if not self._continuing():
            n = 0
            t = 0
            pos = self._init_pos
            vel = self._init_vel
        else:
            n = self._ff_n
            t = self._ff_t
            pos = self._ff_pos
            vel = self._ff_vel

        n_max = None if count is None else n + count

        while True:

            if self._notify(pos, vel, t, n):
                break

            dx1 = dt * vel
            dv1 = dt * self._eq.f(pos=pos, vel=vel, t=t)

            dx2 = dt * (vel+(dv1/2))
            dv2 = dt * self._eq.f(pos=pos+(dx1/2), vel=vel+(dv1/2), t=t+(dt/2))

            dx3 = dt * (vel+(dv2/2))
            dv3 = dt * self._eq.f(pos=pos+(dx2/2), vel=vel+(dv2/2), t=t+(dt/2))

            dx4 = dt * (vel+dv3)
            dv4 = dt * self._eq.f(pos=pos+dx3, vel=vel+dv3, t=t+dt)

            dx = ( dx1 + 2*dx2 + 2*dx3 + dx4 ) / 6
            dv = ( dv1 + 2*dv2 + 2*dv3 + dv4 ) / 6

            pos_n = pos + dx
            vel_n = vel + dv

            # --

            n += 1
            t += dt

            pos = pos_n
            vel = vel_n

            if n_max is not None and n > n_max:
                break

        self._ff_n = n
        self._ff_t = t
        self._ff_pos = pos
        self._ff_vel = vel

        return pos, vel
