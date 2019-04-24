import math
import numpy.linalg as la


class Observer:

    def __init__(self, cfg, ax):
        self._cfg = cfg
        self._ax = ax
        self._closest_src = None
        self._n = 0
        self._len = 0

    def notify(self, pos, vel, t, n):

        # plot probe

        if self._ax is not None:
            if n % self._cfg.m_nProbeModulo == 0:
                self._ax.scatter(pos[0], pos[1], c='k', s=0.01)

        # update _len

        norm_vel = la.norm(vel)

        self._len += norm_vel

        # check for stop condition

        if n < self._cfg.m_nMinSteps:
            return

        if norm_vel > self._cfg.m_fAbortVel:
            return

        b = False
        for src in self._cfg.sources:
            r = pos - src.get_pos()
            if la.norm(r) < src.get_size():
                b = True
                break

        if not b:
            return

        # stop condition satisfied
        # calculate some values

        self._n = n

        closest_dist = None

        for src in self._cfg.sources:

            if not src.get_is_magnet:
                continue

            r = pos - src.get_pos()

            dist = math.sqrt(math.pow(r[0], 2) + math.pow(r[1], 2) + math.pow(self._cfg.m_fHeight, 2))

            if (closest_dist is None) or (dist < closest_dist):
                closest_dist = dist
                self._closest_src = src

        return True

    def get_n(self):
        return self._n

    def get_len(self):
        return self._len

    def get_closest_src(self):
        return self._closest_src