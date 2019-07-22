
import numpy as np
from scipy.integrate import solve_ivp


class SciPy:

    def __init__(self, eq, init_pos, method='RK45'):
        self._eq = eq
        shape = init_pos.shape
        self._n_dim = shape[1]
        self._m_dim = shape[0]
        self._method = method
        self._pos_save = init_pos

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
        res = np.zeros((4, 3))
        for i in range(self._m_dim):
            for j in range(self._n_dim):
                res[i, j] = y[idx]
                idx += 1
        return res

    def _f(self, t, y):
        pos = self._vectorize(y)
        pos = self._eq.f(pos, t)
        pos = self._serialize(pos)
        return pos

    def execute_td(self, t_delta):
        sp = self._serialize(self._pos_save)
        sol = solve_ivp(self._f, [0, t_delta], sp, t_eval=[t_delta], method=self._method, vectorized=True)
        pos = self._vectorize(sol.y)
        self._pos_save = pos
        t = sol.t[0]
        return pos, None, t

    def execute(self, dt, count):
        raise Exception('No available')


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

    def execute_td(self, t_delta):
        dt_count = round(t_delta / self._dt)
        return self.execute(self._dt, dt_count)

    def execute(self, dt, count):

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
