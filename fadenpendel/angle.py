
import integ as it

import numpy as np
import math


class AngleImpl:

    def __init__(self, radius, rho_max):
        self._radius = radius
        self._rho_max = rho_max

    def create_deq(self):
        return it.RungeKutta4th(DiffEq(self._radius), self._rho_max, 0)

    @staticmethod
    def create_frame(integ_ctx, plot_ctx):
        return AnimationFrame(integ_ctx, plot_ctx)


class DiffEq:

    def __init__(self, radius):
        self._radius = radius

    def f(self, pos, vel, t):
        return -(9.81/self._radius)*math.sin(pos)


class AnimationFrame:

    def __init__(self, integ_ctx, plot_ctx):
        self._integ_ctx = integ_ctx
        self._plot_ctx = plot_ctx

        self._rho = None
        self._rhovel = None
        self._rhoacc = None
        self._pos = None
        self._E_pot = None
        self._E_kin = None
        self._F_tan = None
        self._F_zen = None
        self._F_tot = None

    def perform(self):
        self.integrate()
        self.calculate()
        self.cleanup()
        self.plot()

    def integrate(self):
        rho, rhovel, rhoacc = self._integ_ctx.get_deq().execute(self._integ_ctx.get_dt(), self._integ_ctx.get_count())
        self._rho = rho
        self._rhovel = rhovel
        self._rhoacc = rhoacc

    def calculate(self):

        mp_l = self._plot_ctx.get_mp()
        radius_l = self._plot_ctx.get_circle().get_radius()
        m_l = 1
        g_l = 9.81

        # - position of the pendulum

        pos = self._plot_ctx.get_circle().calc(self._rho)
        self._pos = pos

        # - radialer einheitsvektor e_r

        e_r = (mp_l - pos) / radius_l

        # - tangentialer einheitsvektor e_t

        z = pos[2]
        x = -(e_r[2] * z / (e_r[0] + e_r[1] * (pos[1] / pos[0])))
        y = (pos[1] / pos[0]) * x

        e_t = np.array([x, y, z])

        if self._rho < 0:
            e_t = e_t * (-1)

        e_t = e_t / math.sqrt(math.pow(e_t[0], 2) + math.pow(e_t[1], 2) + math.pow(e_t[2], 2))

        # - velocity

        vel = self._rhovel * radius_l

        # - Energies

        # E_pot = m * g * l * (1 - cos(rho))
        self._E_pot = m_l * g_l * (radius_l - (radius_l * math.cos(self._rho)))

        # E_kin = (1/2) * m * v^2
        self._E_kin = (1/2) * g_l * math.pow(vel, 2)

        # - Forces

        # F_tan = m * g * sin(rho)
        self._F_tan = - m_l * g_l * math.sin(self._rho) * e_t

        # F_zen = ( m * v^2 ) / radius
        self._F_zen = ( ( m_l * math.pow(vel, 2) ) / radius_l ) * e_r

        # F_tot = F_tan + F_zen
        self._F_tot = ( self._F_tan + self._F_zen )

    def cleanup(self):

        ax_l = self._plot_ctx.get_ax()

        artist = self._plot_ctx.get_line()
        if artist is None:
            artist, = ax_l.plot([], [], [], lw=0.5)
            self._plot_ctx.set_line(artist)

        artist = self._plot_ctx.get_mass()
        if artist is None:
            artist, = ax_l.plot([], [], [], "o", markersize=5, color=(0,0,0))
            self._plot_ctx.set_mass(artist)

        for artist in self._plot_ctx.get_artists():
            artist.remove()

    def plot(self):

        artists = []

        ax_l = self._plot_ctx.get_ax()
        mp_l = self._plot_ctx.get_mp()

        pos = self._pos

        # line plot

        artist = self._plot_ctx.get_line()
        artist.set_data([mp_l[0], pos[0]], [mp_l[1], pos[1]])
        artist.set_3d_properties([mp_l[2], pos[2]])

        # mass plot

        artist = self._plot_ctx.get_mass()
        artist.set_data(pos[0], pos[1])
        artist.set_3d_properties(pos[2])

        E_pot_norm = (self._E_pot/(self._E_pot+self._E_kin))
        E_kin_norm = 1-E_pot_norm

        artist.set_color(color=(E_pot_norm,0,E_kin_norm))

        artist.set_zorder(20)

        # forces

        artist = ax_l.quiver(pos[0], pos[1], pos[2], self._F_zen[0], self._F_zen[1], self._F_zen[2])
        artists.append(artist)

        artist = ax_l.quiver(pos[0], pos[1], pos[2], self._F_tan[0], self._F_tan[1], self._F_tan[2])
        artists.append(artist)

        artist = ax_l.quiver(pos[0], pos[1], pos[2], self._F_tot[0], self._F_tot[1], self._F_tot[2])
        artists.append(artist)

        # done
        self._plot_ctx.set_artists(artists)
