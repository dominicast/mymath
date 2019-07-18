

class RungeKutta4th:

    def __init__(self, eq, init_pos):
        self._eq = eq
        self._init_pos = init_pos

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
