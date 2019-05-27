
from utils import *

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import juggle_axes
from matplotlib import animation
import numpy as np
import math
import integ as it


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

        artist = self._plot_ctx.get_line()
        if artist is None:
            artist, = ax.plot([], [], [], lw=0.5)
            self._plot_ctx.set_line(artist)

        artist = self._plot_ctx.get_mass()
        if artist is None:
            artist, = ax.plot([], [], [], "o", markersize=5, color=(0,0,0))
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


def animate(i, integ_ctx, plot_ctx):
    AnimationFrame(integ_ctx, plot_ctx).perform()


if __name__ == '__main__':

    radius = 10

    rho_max = math.radians(40)

    phi = math.radians(45)

    time_factor = 1

    # -- situation

    # mount point
    mp = np.array([0, 0, radius+(radius/10)])

    # circle
    circle = Circle(radius, mp, phi)

    # -- integration

    deq = it.RungeKutta4th(DiffEq(radius), rho_max, 0)

    integ_dt = 0.01    # [s]
    integ_count = 10
    integ_freq = 100   # [ms]

    if integ_dt * integ_count * 1000 != integ_freq:
        print('Invalid time configuration')

    integ_count = round(integ_count * time_factor)

    integ_ctx = IntegrationCtx(deq, integ_dt, integ_count)

    # -- setup plot

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.set_xlabel('x', fontsize=15)
    ax.set_xlim3d(-radius, radius)

    ax.set_ylabel('y', fontsize=15)
    ax.set_ylim3d(-radius, radius)

    ax.set_zlabel('z', fontsize=15)
    ax.set_zlim3d(0, radius+2*(radius/10))

    plot_ctx = PlotCtx(ax, mp, circle)

    # -- plot frame

    # vertical line
    ax.plot(np.array([0, mp[0]]), np.array([0, mp[1]]), np.array([mp[2]-radius, mp[2]]), c='k', lw=0.5)

    # mount point
    ax.scatter(mp[0], mp[1], mp[2], c='r')

    # expected circle
    pp = circle.calc(rho_max)
    rho_tmp = rho_max - math.radians(5)
    while rho_tmp >= -(rho_max + math.pi / 1000):
        pn = circle.calc(rho_tmp)
        ax.plot(np.array([pp[0], pn[0]]), np.array([pp[1], pn[1]]), np.array([pp[2], pn[2]]), c='k', lw=0.5)
        pp = pn
        rho_tmp -= math.radians(5)

    # -- run

    anim = animation.FuncAnimation(fig, animate, interval=integ_freq, fargs=(integ_ctx,plot_ctx,), blit=False)

    plt.show()
