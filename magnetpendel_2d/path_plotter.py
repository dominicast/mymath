
import numpy as np


class Plotter:

    def __init__(self, ax):
        self._ax = ax
        self._last_pos = None
        self._artists = []

    def setup(self, width, height):

        ax = self._ax

        ax.set_title('Magnetpendel 2D Path')

        ax.set_xlabel('x', fontsize=15)
        ax.set_xlim(-width, width)

        ax.set_ylabel('y', fontsize=15)
        ax.set_ylim(-height, height)

        ax.grid(True)

    def plot_situation(self, magnets):

        ax = self._ax

        for magnet in magnets:
            ax.scatter(magnet.get_pos()[0], magnet.get_pos()[1], c=magnet.get_color(), s=magnet.get_size() * 50)

    def plot_frame(self, data):
        if data is None:
            return
        self._cleanup(data)
        self._plot_frame(data)

    def _cleanup(self, data):
        for artist in self._artists:
            artist.remove()

    def _plot_frame(self, data):

        ax = self._ax

        pos = data.get_pos()

        if self._last_pos is not None:
            lp = self._last_pos
            ax.plot(np.array([lp[0], pos[0]]), np.array([lp[1], pos[1]]), c='k', lw=0.5)

        self._last_pos = pos

        if data.get_done() and data.get_found():
            pos = data.get_source().get_pos()
            ax.scatter(pos[0], pos[1], c='y', s=140, marker="x", zorder=101)
