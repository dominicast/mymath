
class Plotter:

    def __init__(self, ax, point_size):
        self._ax = ax
        self._point_size = point_size

    def setup(self, width, height):

        ax = self._ax

        ax.set_title('Magnetpendel 2D Pattern')

        ax.set_xlabel('x', fontsize=15)
        ax.set_xlim(-width, width)

        ax.set_ylabel('y', fontsize=15)
        ax.set_ylim(-height, height)

        ax.grid(False)

    def plot_point(self, point):

        ax = self._ax

        if point.get_found():
            alpha = 1
        else:
            alpha = 0.5

        ax.scatter(point.get_x(), point.get_y(), c=point.get_color(), s=self._point_size, alpha=alpha)
