
import integ as it

import numpy as np
import math


class ForceImpl:

    def __init__(self, mp, sp, plot_ctx):
        self._mp = mp
        self._sp = sp
        self._plot_ctx = plot_ctx

    def create_deq(self):
        return it.RungeKutta4th(DiffEq(self._mp, self._plot_ctx), self._sp, np.array([0, 0, 0]))

    @staticmethod
    def create_frame(integ_ctx, plot_ctx):
        return AnimationFrame(integ_ctx, plot_ctx)


class DiffEq:

    def __init__(self, mp, plot_ctx):
        self._mp = mp
        self._plot_ctx = plot_ctx

    def f(self, pos, vel, t):

        for artist in self._plot_ctx.get_artists():
            artist.remove()

        artists = []

        ax_l = self._plot_ctx.get_ax()

        # reverse radius vector

        rr = (self._mp - pos)
        rr_len = math.sqrt(math.pow(rr[0],2)+math.pow(rr[1],2)+math.pow(rr[2],2))

        # radialer einheitsvektor e_r

        e_r = (self._mp - pos) / rr_len

        # tangentialer einheitsvektor e_t

        z = pos[2]
        x = -(e_r[2] * z / (e_r[0] + e_r[1] * (pos[1] / pos[0])))
        y = (pos[1] / pos[0]) * x

        e_t = np.array([x, y, z])

        e_t = e_t / math.sqrt(math.pow(e_t[0], 2) + math.pow(e_t[1], 2) + math.pow(e_t[2], 2))

        # ---

        m_l = 1
        g_l = 9.81

        # F_tan = m * g * sin(rho)

        rho = math.acos(e_t[0]*e_r[0] + e_t[1]*e_r[1] + e_t[2]*e_r[2])
        F_tan = - m_l * g_l * math.sin(rho) * e_t

        # F_zen = ( m * v^2 ) / radius

        vel_len = math.sqrt(math.pow(vel[0],2)+math.pow(vel[1],2)+math.pow(vel[2],2))
        F_zen = ( ( m_l * math.pow(vel_len, 2) ) / rr_len ) * e_r

        # F_tot

        F_tot = ( F_tan + F_zen )

        # plot

        artist = ax_l.quiver(pos[0], pos[1], pos[2], F_zen[0], F_zen[1], F_zen[2])
        artists.append(artist)

        artist = ax_l.quiver(pos[0], pos[1], pos[2], F_tan[0], F_tan[1], F_tan[2])
        artists.append(artist)

        artist = ax_l.quiver(pos[0], pos[1], pos[2], F_tot[0], F_tot[1], F_tot[2])
        artists.append(artist)

        self._plot_ctx.set_artists(artists)

        return F_tot


class AnimationFrame:

    def __init__(self, integ_ctx, plot_ctx):
        self._integ_ctx = integ_ctx
        self._plot_ctx = plot_ctx

        self._rho = None
        self._rhovel = None
        self._pos = None
        self._vv = None
        self._F_t = None

    def perform(self):
        self.integrate()
        self.cleanup()
        self.plot()

    def integrate(self):
        pos, vel, acc = self._integ_ctx.get_deq().execute(self._integ_ctx.get_dt(), self._integ_ctx.get_count())
        self._pos = pos
        self._vel = vel
        self._acc = acc

    def cleanup(self):

        ax_l = self._plot_ctx.get_ax()

        artist = self._plot_ctx.get_line()
        if artist is None:
            artist, = ax_l.plot([], [], [], lw=0.5)
            self._plot_ctx.set_line(artist)

        artist = self._plot_ctx.get_mass()
        if artist is None:
            artist, = ax_l.plot([], [], [], "o", markersize=5)
            self._plot_ctx.set_mass(artist)

    def plot(self):

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
