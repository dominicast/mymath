
import math
import numpy as np


class Circle:

    def __init__(self, radius, mp, phi):
        self._radius = radius
        self._mp = mp
        self._phi = phi

    def calc(self, rho):
        # Kuegelkoordinaten

        x = self._radius * math.sin(rho) * math.cos(self._phi)
        y = self._radius * math.sin(rho) * math.sin(self._phi)
        z = self._radius * math.cos(rho)

        v = np.array([x, y, z])
        v[2] = -v[2]
        v = self._mp + v

        return v

    def get_radius(self):
        return self._radius


class IntegrationCtx:

    def __init__(self, deq, dt, count):
        self._deq = deq
        self._dt = dt
        self._count = count

    def get_deq(self):
        return self._deq

    def get_dt(self):
        return self._dt

    def get_count(self):
        return self._count


class PlotCtx:

    def __init__(self, ax, mp, circle):
        self._ax = ax
        self._mp = mp
        self._circle = circle

        self._mass = None
        self._line = None
        self._artists = []

    def get_ax(self):
        return self._ax

    def get_mp(self):
        return self._mp

    def get_circle(self):
        return self._circle

    def get_mass(self):
        return self._mass

    def set_mass(self, mass):
        self._mass = mass

    def get_line(self):
        return self._line

    def set_line(self, line):
        self._line = line

    def get_artists(self):
        return self._artists

    def set_artists(self, artists):
        self._artists = artists


class FrameData:

    def __init__(self, pos, mp, F_zen, F_tan, F_tot, E_pot, E_kin):
        self._pos = pos
        self._mp = mp
        self._F_zen = F_zen
        self._F_tan = F_tan
        self._F_tot = F_tot
        self._E_pot = E_pot
        self._E_kin = E_kin

    def get_pos(self):
        return self._pos

    def get_mp(self):
        return self._mp

    def get_F_zen(self):
        return self._F_zen

    def get_F_tan(self):
        return self._F_tan

    def get_F_tot(self):
        return self._F_tot

    def get_E_pot(self):
        return self._E_pot

    def get_E_kin(self):
        return self._E_kin
