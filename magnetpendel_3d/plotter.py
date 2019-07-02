
import numpy as np


class FrameData:

    def __init__(self, pos, mp, m):
        self._pos = pos
        self._mp = mp
        self._m = m

    def get_pos(self):
        return self._pos

    def get_mp(self):
        return self._mp

    def get_m(self):
        return self._m


class Plotter:

    def __init__(self, ax, mp):
        self._ax = ax
        self._mp = mp

        self._mass = None
        self._line = None
        self._artists = []

        self._last_pos = None

    def setup(self, width, height, depth):

        ax = self._ax

        ax.set_title('Magnetpendel 3D')

        ax.set_xlabel('x', fontsize=15)
        ax.set_xlim3d(-width, width)

        ax.set_ylabel('y', fontsize=15)
        ax.set_ylim3d(-height, height)

        ax.set_zlabel('z', fontsize=15)
        ax.set_zlim3d(0, depth)

    def plot_situation(self, mount_point, magnets):

        ax = self._ax

        pos = mount_point.get_pos()
        artist, = ax.plot([], [], [], "o", markersize=5, color=mount_point.get_color())
        artist.set_data(pos[0], pos[1])
        artist.set_3d_properties(pos[2])

        for magnet in magnets:
            pos = magnet.get_pos()
            artist, = ax.plot([], [], [], "x", markersize=(magnet.get_size()*200), color=magnet.get_color())
            artist.set_data(pos[0], pos[1])
            artist.set_3d_properties(pos[2])

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

        # line plot

        self._line.set_data([mp[0], pos[0]], [mp[1], pos[1]])
        self._line.set_3d_properties([mp[2], pos[2]])
        self._line.set_zorder(99)

        # mass plot

        self._mass.set_data(pos[0], pos[1])
        self._mass.set_3d_properties(pos[2])
        self._mass.set_zorder(99)

        # path plot

        if self._last_pos is not None:
            lp = self._last_pos
            ax.plot(np.array([lp[0], pos[0]]), np.array([lp[1], pos[1]]), np.array([lp[2], pos[2]]), c='silver', lw=0.5)

        self._last_pos = pos

        # done
        self._artists = artists
