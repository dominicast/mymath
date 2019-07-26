
import numpy as np
from scipy.integrate import solve_ivp


class SciPy:

    def __init__(self, eq, init_pos, method='RK45', logger=None):
        self._logger = logger
        self._eq = eq
        self._log('o1_init', ('init_pos', init_pos))
        shape = init_pos.shape
        self._n_dim = shape[1]
        self._m_dim = shape[0]
        self._method = method
        self._pos_save = init_pos

    def _log(self, tag, *values, level=None):
        if self._logger is not None:
            self._logger.log(tag, *values, level=level)

    def _inc_log_level(self):
        if self._logger is not None:
            self._logger.inc_level()

    def _dec_log_level(self):
        if self._logger is not None:
            self._logger.dec_level()

    def _serialize(self, y):
        res = np.zeros(self._m_dim * self._n_dim)
        idx = 0
        for i in range(self._m_dim):
            for j in range(self._n_dim):
                res[idx] = y[i, j]
                idx += 1
        return res

    def _vectorize(self, y):
        idx = 0
        res = np.zeros((self._m_dim, self._n_dim))
        for i in range(self._m_dim):
            for j in range(self._n_dim):
                res[i, j] = y[idx]
                idx += 1
        return res

    def _f(self, t, y):

        self._inc_log_level()

        self._log('o1_f_1', ('y', y))

        pos = self._vectorize(y)

        self._log('o1_f_2', ('pos', pos))

        pos = self._eq.f(pos, t)

        self._log('o1_f_3', ('pos', pos))

        pos = self._serialize(pos)

        self._log('o1_f_4', ('pos', pos))

        self._dec_log_level()

        return pos

    def process_td(self, t_delta):

        self._inc_log_level()

        sp = self._serialize(self._pos_save)

        self._log('o1_process_1', ('sp', sp))

        sol = solve_ivp(self._f, [0, t_delta], sp, t_eval=[t_delta], method=self._method, vectorized=True)

        self._log('o1_process_2', ('sol.y', sol.y))

        pos = self._vectorize(sol.y)

        self._log('o1_process_3', ('pos', pos))

        self._pos_save = pos

        t = sol.t[0]

        self._dec_log_level()

        return pos, None, t

    def process_dt(self, count):
        raise Exception('Not available')


class RungeKutta4th:

    def __init__(self, eq, init_pos, dt):
        self._eq = eq
        self._init_pos = init_pos
        self._dt = dt

        self._ff_n = None
        self._ff_t = None
        self._ff_pos = None

    def _continuing(self):
        if self._ff_n is None:
            return False
        if self._ff_t is None:
            return False
        if self._ff_pos is None:
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
        else:
            n = self._ff_n
            t = self._ff_t
            pos = self._ff_pos

        n_max = None if count is None else n + count

        while True:

            k1 = dt * self._eq.f(pos, t)
            k2 = dt * self._eq.f(pos+(k1/2), t+(dt/2))
            k3 = dt * self._eq.f(pos+(k2/2), t+(dt/2))
            k4 = dt * self._eq.f(pos+k3, t+dt)

            dp = ( k1 + 2*k2 + 2*k3 + k4 ) / 6

            pos_n = pos + dp

            # --

            n += 1
            t += dt

            pos = pos_n

            if n_max is not None and n >= n_max:
                break

        self._ff_n = n
        self._ff_t = t
        self._ff_pos = pos

        return pos, dp, t
