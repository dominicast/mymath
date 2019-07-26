import math
import numpy as np
from integ1o import SciPy as SciPy1O


class SciPyAdapterSkalar:

    @staticmethod
    def get_dims(pos):
        m_dim = 1
        n_dim = 1
        return m_dim, n_dim

    @staticmethod
    def serialize_get(value, idx):
        return value

    @staticmethod
    def vectorize_get(value):
        return value[0][0]


class SciPyAdapterVector:

    @staticmethod
    def get_dims(pos):
        shape = pos.shape
        m_dim = 1
        n_dim = shape[0]
        return m_dim, n_dim

    @staticmethod
    def serialize_get(value, idx):
        return value

    @staticmethod
    def vectorize_get(value):
        return value[0]


class SciPyAdapterMatrix:

    @staticmethod
    def get_dims(pos):
        shape = pos.shape
        m_dim = shape[0]
        n_dim = shape[1]
        return m_dim, n_dim

    @staticmethod
    def serialize_get(value, idx):
        return value[idx]

    @staticmethod
    def vectorize_get(value):
        return value


class SciPyAdapterFactory:

    @staticmethod
    def create(value):
        if type(value) is float:
            return SciPyAdapterSkalar()
        elif type(value) is np.ndarray:
            if len(value.shape) == 1:
                return SciPyAdapterVector()
            elif len(value.shape) > 1:
                return SciPyAdapterMatrix()
            else:
                raise Exception('unknown shape ' + repr(value.shape))
        else:
            raise Exception('unknown type '+repr(type(value)))


class SciPyLogger:

    def __init__(self, log_level):
        self._log_level = log_level
        self._ident_level = 0

    def inc_level(self):
        self._ident_level += 1

    def dec_level(self):
        self._ident_level -= 1

    def log(self, tag, *values, level=None):
        if level is None:
            level = self._ident_level
        if level > self._log_level:
            return

        ident = ' '*self._ident_level*3

        # header
        ending = '-'*(30-len(tag))
        str = ident+'- '+tag+' '+ending
        print(str)

        # body
        for value in values:
            print(ident+repr(value[0])+': '+repr(value[1]).replace('\n', '|'))

        # footer
        print(ident+'-'*33)


class SciPy:

    def __init__(self, eq, init_pos, init_vel, method='RK45', adapter=None, logger=None):
        if adapter is not None:
            self._adapter = adapter
        else:
            self._adapter = SciPyAdapterFactory.create(init_pos)
        self._logger = logger
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel
        self._log('o2_init', ('init_pos', self._init_pos), ('init_vel', self._init_vel))
        m_dim, n_dim = self._adapter.get_dims(init_pos)
        self._m_dim = m_dim
        self._n_dim = n_dim
        self._method = method
        self._solver = None

    def _log(self, tag, *values, level=None):
        if self._logger is not None:
            self._logger.log(tag, *values, level=level)

    def _inc_log_level(self):
        if self._logger is not None:
            self._logger.inc_level()

    def _dec_log_level(self):
        if self._logger is not None:
            self._logger.dec_level()

    def _serialize(self, p, v):
        res = np.zeros((2 * self._m_dim , self._n_dim))
        idx = 0
        for i in range(self._m_dim):
            for j in range(2):
                if j == 0:
                    res[idx] = self._adapter.serialize_get(p, i)
                else:
                    res[idx] = self._adapter.serialize_get(v, i)
                idx += 1
        return res

    def _vectorize(self, y):
        idx = 0
        pos = np.zeros((self._m_dim, self._n_dim))
        vel = np.zeros((self._m_dim, self._n_dim))
        for i in range(self._m_dim):
            pos[i] = y[idx]
            idx += 1
            vel[i] = y[idx]
            idx += 1
        pos = self._adapter.vectorize_get(pos)
        vel = self._adapter.vectorize_get(vel)
        return pos, vel

    def _f(self, t, y):

        self._inc_log_level()

        self._log('o2_f_1', ('y', y))

        pos, vel = self._vectorize(y)

        self._log('o2_f_2', ('pos', pos), ('vel', vel))

        pos = self._eq.f(pos, vel, t)

        self._log('o2_f_3', ('pos', pos), ('vel', vel))

        pos = self._serialize(vel, pos)

        self._log('o2_f_3', ('pos', pos), ('vel', vel), ('t', t))

        self._dec_log_level()

        return pos

    def process_td(self, t_delta):

        if self._solver is None:
            sp = self._serialize(self._init_pos, self._init_vel)
            self._log('o2_process_0', ('sp', sp))
            self._solver = SciPy1O(SciPyDeq(self), sp, method=self._method, logger=self._logger)

        self._inc_log_level()

        sol, _, t = self._solver.process_td(t_delta)

        self._log('o2_process_1', ('sol', sol))

        pos, vel = self._vectorize(sol)

        self._log('o2_process_2', ('pos', pos), ('vel', vel), ('t', t))

        self._dec_log_level()

        return pos, vel, None, t

    def process_dt(self, dt, count):
        raise Exception('Not available')


class SciPyDeq:

    def __init__(self, solver):
        self._solver = solver

    def f(self, pos, t):
        return self._solver._f(t, pos)


# Jorge Rodriguez (14.07.2016)
# Math for Game Developers - Spaceship Orbits (Semi-Implicit Euler)
# https://www.youtube.com/watch?v=kxWBXd7ujx0
class EulerBase:

    def __init__(self, eq, init_pos, init_vel, dt):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel
        self._dt = dt

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

    def process_td(self, t_delta):
        dt_count = round(t_delta / self._dt)
        return self._process(self._dt, dt_count)

    def process_dt(self, count):
        return self._process(self._dt, count)

    def _process(self, dt, count):

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

            acc = self._eq.f(pos, vel, t)

            vel_n = vel + dt * acc

            #if n % 100 == 0:
            #    print( '('+repr(pos[0])+','+repr(pos[1])+','+repr(pos[2])+') - ('+repr(vel[0])+','+repr(vel[1])+','+repr(vel[2])+')' )

            pos_n = pos + dt * self._chose_velocity(vel, vel_n)

            # --

            n += 1
            t += dt
            vel = vel_n
            pos = pos_n

            if n_max is not None and n >= n_max:
                break

        self._ff_n = n
        self._ff_t = t
        self._ff_pos = pos
        self._ff_vel = vel

        return pos, vel, acc, t


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

    def __init__(self, eq, init_pos, init_vel, dt):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel
        self._dt = dt

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

    def process_td(self, t_delta):
        dt_count = round(t_delta / self._dt)
        return self._process(self._dt, dt_count)

    def process_dt(self, count):
        return self._process(self._dt, count)

    def _process(self, dt, count):

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

            vel_mp = vel + (dt/2) * self._eq.f(pos, vel, t)
            vel_n = vel + dt * self._eq.f(pos, vel_mp, t+(dt/2))

            pos_n = pos + dt * vel_n

            # --

            n += 1
            t += dt

            vel = vel_n
            pos = pos_n

            if n_max is not None and n >= n_max:
                break

        self._ff_n = n
        self._ff_t = t
        self._ff_pos = pos
        self._ff_vel = vel

        return pos, vel, None, t


# Jorge Rodriguez (21.07.2016)
# Math for Game Developers - Verlet Integration
# https://www.youtube.com/watch?v=AZ8IGOHsjBk
class Verlet:

    def __init__(self, eq, init_pos, init_vel, dt):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel
        self._dt = dt

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

    def process_td(self, t_delta):
        dt_count = round(t_delta / self._dt)
        return self._process(self._dt, dt_count)

    def process_dt(self, count):
        return self._process(self._dt, count)

    def _process(self, dt, count):

        dt_rez=(1/dt)

        if not self._continuing():

            # --

            n = 0
            t = 0

            pos = self._init_pos
            vel = self._init_vel
            acc = self._eq.f(pos, vel, t)

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
            acc = self._eq.f(pos, vel, t)

            pos_n = 2 * pos - pos_p + acc * math.pow(dt, 2)

            # --

            n += 1
            t += dt

            pos_p = pos
            pos = pos_n

            if n_max is not None and n >= n_max:
                break

        self._ff_n = n
        self._ff_t = t
        self._ff_pos = pos
        self._ff_pos_p = pos_p

        return pos, vel, acc, t


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

    def __init__(self, eq, init_pos, init_vel, dt):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel
        self._dt = dt

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

    def process_td(self, t_delta):
        dt_count = round(t_delta / self._dt)
        return self._process(self._dt, dt_count)

    def process_dt(self, count):
        return self._process(self._dt, count)

    def _process(self, dt, count):

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

        while True:

            n += 1
            t += dt

            if n_max is not None and n >= n_max:
                break

            pos = pos + vel * dt + math.pow( dt, 2 ) * ( (2/3) * acc - (1/6) * acc_p )

            acc_n = self._eq.f(pos, vel, t)

            vel = vel + dt * ( (1/3) * acc_n + (5/6) * acc - (1/6) * acc_p )

            acc_p = acc
            acc = acc_n

        self._ff_n = n
        self._ff_t = t
        self._ff_pos = pos
        self._ff_vel = vel
        self._ff_acc = acc
        self._ff_acc_p = acc_p

        return pos, vel, acc, t


# Jorge Rodriguez (04.08.2016)
# Math for Game Developers - Runge-Kutta Order 4
# https://www.youtube.com/watch?v=hGCP6I2WisM
#
# Aleksandr Spiridonov (29.04.2011)
# Runge Kutta 4th order method for ODE2
# https://www.youtube.com/watch?v=smfX0Jt_f0I
class RungeKutta4th:

    def __init__(self, eq, init_pos, init_vel, dt):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel
        self._dt = dt

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

    def process_td(self, t_delta):
        dt_count = round(t_delta / self._dt)
        return self._process(self._dt, dt_count)

    def process_dt(self, count):
        return self._process(self._dt, count)

    def _process(self, dt, count):

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

            dx1 = dt * vel
            dv1 = dt * self._eq.f(pos, vel, t)

            dx2 = dt * (vel+(dv1/2))
            dv2 = dt * self._eq.f(pos+(dx1/2), vel+(dv1/2), t+(dt/2))

            dx3 = dt * (vel+(dv2/2))
            dv3 = dt * self._eq.f(pos+(dx2/2), vel+(dv2/2), t+(dt/2))

            dx4 = dt * (vel+dv3)
            dv4 = dt * self._eq.f(pos+dx3, vel+dv3, t+dt)

            dx = ( dx1 + 2*dx2 + 2*dx3 + dx4 ) / 6
            dv = ( dv1 + 2*dv2 + 2*dv3 + dv4 ) / 6

            pos_n = pos + dx
            vel_n = vel + dv

            # --

            n += 1
            t += dt

            pos = pos_n
            vel = vel_n

            if n_max is not None and n >= n_max:
                break

        self._ff_n = n
        self._ff_t = t
        self._ff_pos = pos
        self._ff_vel = vel

        return pos, vel, dv, t
