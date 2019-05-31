
from utils import *
from angle import AngleImpl
from force import ForceImpl
from config import *

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import juggle_axes
from matplotlib import animation
import numpy as np
import math


class Plotter:

    def __init__(self, plot_ctx, data):
        self._plot_ctx = plot_ctx
        self._data = data

    def perform(self):
        self.cleanup()
        self.plot()

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

        pos = self._data.get_pos()

        E_pot = self._data.get_E_pot()
        E_kin = self._data.get_E_kin()

        F_zen = self._data.get_F_zen()
        F_tan = self._data.get_F_tan()
        F_tot = self._data.get_F_tot()

        # line plot

        artist = self._plot_ctx.get_line()
        artist.set_data([mp_l[0], pos[0]], [mp_l[1], pos[1]])
        artist.set_3d_properties([mp_l[2], pos[2]])

        # mass plot

        artist = self._plot_ctx.get_mass()
        artist.set_data(pos[0], pos[1])
        artist.set_3d_properties(pos[2])

        if E_pot is not None and E_kin is not None:
            E_pot_norm = (E_pot/(E_pot+E_kin))
            E_kin_norm = 1-E_pot_norm
            c = (E_pot_norm,0,E_kin_norm)
        else:
            c = 'r'

        artist.set_color(color=c)

        artist.set_zorder(20)

        # forces

        if F_zen is not None:
            artist = ax_l.quiver(pos[0], pos[1], pos[2], F_zen[0], F_zen[1], F_zen[2])
            artists.append(artist)

        if F_tan is not None:
            artist = ax_l.quiver(pos[0], pos[1], pos[2], F_tan[0], F_tan[1], F_tan[2])
            artists.append(artist)

        if F_tot is not None:
            artist = ax_l.quiver(pos[0], pos[1], pos[2], F_tot[0], F_tot[1], F_tot[2])
            artists.append(artist)

        # done
        self._plot_ctx.set_artists(artists)


def animate(i, integ_ctx, plot_ctx, impl):
    frame = impl.create_frame(integ_ctx)
    data = frame.perform()
    plotter = Plotter(plot_ctx, data)
    plotter.perform()


if __name__ == '__main__':

    config = Config()

    radius = config.get_radius()
    rho_max = config.get_rho_max()
    time_factor = config.get_time_factor()

    # -- situation

    # mount point
    mp = np.array([0, 0, radius+(radius/10)])

    # circle
    circle = Circle(radius, mp, rho_max)

    # start point
    sp = circle.calc(rho_max)

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

    # -- implementation

    if config.get_impl() == Impl.ANGLE:
        impl = AngleImpl(radius, rho_max)
    elif config.get_impl() == Impl.FORCE:
        impl = ForceImpl(mp, sp, 1, 9.81)
    else:
        raise Exception('Unknown implementation')

    # -- integration

    deq = impl.create_deq()

    integ_dt = config.get_integ_dt()
    integ_count = config.get_integ_count()
    integ_freq = config.get_integ_freq()

    if integ_dt * integ_count * 1000 != integ_freq:
        print('Invalid time configuration')

    integ_count = round(integ_count * time_factor)

    integ_ctx = IntegrationCtx(deq, integ_dt, integ_count)

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

    anim = animation.FuncAnimation(fig, animate, interval=integ_freq, fargs=(integ_ctx,plot_ctx,impl,), blit=False)

    plt.show()
