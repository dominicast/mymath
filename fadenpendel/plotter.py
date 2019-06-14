
import math
import numpy as np


class Plotter:

    def __init__(self, ax, mp):
        self._ax = ax
        self._mp = mp

        self._mass = None
        self._line = None
        self._artists = []

    def setup(self, radius):

        ax = self._ax

        ax.set_xlabel('x', fontsize=15)
        ax.set_xlim3d(-radius, radius)

        ax.set_ylabel('y', fontsize=15)
        ax.set_ylim3d(-radius, radius)

        ax.set_zlabel('z', fontsize=15)
        ax.set_zlim3d(0, radius + 2 * (radius / 10))

    def plot_situation(self, circle, rho_max):

        ax = self._ax

        mp = self._mp

        radius = circle.get_radius()

        # vertical line
        ax.plot(np.array([0, mp[0]]), np.array([0, mp[1]]), np.array([mp[2] - radius, mp[2]]), c='k', lw=0.5)

        # mount point
        ax.scatter(mp[0], mp[1], mp[2], c='darkgoldenrod')

        # expected circle
        pp = circle.calc(rho_max)
        rho_tmp = rho_max - math.radians(5)
        while rho_tmp >= -(rho_max + math.pi / 1000):
            pn = circle.calc(rho_tmp)
            ax.plot(np.array([pp[0], pn[0]]), np.array([pp[1], pn[1]]), np.array([pp[2], pn[2]]), c='k', lw=0.5)
            pp = pn
            rho_tmp -= math.radians(5)

    def plot_frame(self, data):
        if data is None:
            return
        self._cleanup(data)
        self._plot_frame(data)

    def _cleanup(self, data):

        ax = self._ax

        if self._line is None:
            self._line, = ax.plot([], [], [], lw=0.5)

        if self._mass is None:
            self._mass, = ax.plot([], [], [], "o", markersize=(5*data.get_m()), color=(0,0,0))

        for artist in self._artists:
            artist.remove()

    def _plot_frame(self, data):

        artists = []

        ax = self._ax

        pos = data.get_pos()
        mp = data.get_mp()

        E_pot = data.get_E_pot()
        E_kin = data.get_E_kin()

        F_zen = data.get_F_zen()
        F_tan = data.get_F_tan()
        F_d = data.get_F_d()
        F_tot = data.get_F_tot()

        # line plot

        self._line.set_data([mp[0], pos[0]], [mp[1], pos[1]])
        self._line.set_3d_properties([mp[2], pos[2]])

        # mass plot

        self._mass.set_data(pos[0], pos[1])
        self._mass.set_3d_properties(pos[2])

        if E_pot is not None and E_kin is not None:

            c_pot = np.array([0.725, 0.522, 0.27])
            c_kin = np.array([0, 0, 0])

            E_pot_norm = (E_pot/(E_pot+E_kin))
            E_kin_norm = 1-E_pot_norm

            c_r = E_pot_norm*c_pot[0] + E_kin_norm*c_kin[0]
            c_g = E_pot_norm*c_pot[1] + E_kin_norm*c_kin[1]
            c_b = E_pot_norm*c_pot[2] + E_kin_norm*c_kin[2]

            c = (c_r, c_g, c_b)
        else:
            c = 'r'

        self._mass.set_color(color=c)

        self._mass.set_zorder(20)

        # forces

        if F_zen is not None:
            artist = ax.quiver(pos[0], pos[1], pos[2], F_zen[0], F_zen[1], F_zen[2], alpha=0.7)
            artist.set_zorder(18)
            artists.append(artist)

        if F_tan is not None:
            artist = ax.quiver(pos[0], pos[1], pos[2], F_tan[0], F_tan[1], F_tan[2], alpha=0.7)
            artist.set_zorder(18)
            artists.append(artist)

        if F_d is not None:
            artist = ax.quiver(pos[0], pos[1], pos[2], F_d[0], F_d[1], F_d[2], alpha=0.7)
            artist.set_zorder(18)
            artists.append(artist)

        if F_tot is not None:
            artist = ax.quiver(pos[0], pos[1], pos[2], F_tot[0], F_tot[1], F_tot[2], color='darkgoldenrod', alpha=1)
            artist.set_zorder(19)
            artists.append(artist)

        # done
        self._artists = artists
