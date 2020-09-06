import math
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
import integ as it
from enum import Enum

import matplotlib.pyplot as plt
from matplotlib import animation

# Solved the following equation
#
# ddot(vec(x)) = sum(G*((m_{body})/(abs(vec(r))^3))*vec(r))
# vec(x): Path
# G: Universal gravitational constant ( 6.67408E-11 m^3 * kg^-1 * s^-2)
# m_{body}: Mass of the attracting body
# vec(r): Vector from current position the the attracting body
#
# http://asciimath.org/

class Body:

    def __init__(self, pos, size):
        self._pos = pos
        self._size = size

    def get_pos(self):
        return self._pos

    def get_size(self):
        return self._size

class DiffEq:

    def f( self, pos, vel, t ):
        result = np.array([0,0])

        G = 0.1    # yes thats not the real value
        rexp = 1   # 1 for convenience - should be 3

        for b in bodies:

            r = b.get_pos() - pos

            m = b.get_size()
            rn = la.norm(r)
            rnq = math.pow( rn, rexp )

            fact = G * ( m / rnq )

            result = result + fact * r

        return result

class Plotter:

    def __init__(self, ax):
        self._ax = ax
        self._last_pos = None
        self._artists = []

    def setup(self):
        ax.set_title('Path')

        ax.set_xlabel('x', fontsize=15)
        ax.set_xlim(0, 100)

        ax.set_ylabel('y', fontsize=15)
        ax.set_ylim(0, 100)

        ax.grid(True)

    def plot_situation(self, init_pos, init_vel, bodies):
        ax = self._ax

        for b in bodies:
            ax.scatter(b.get_pos()[0], b.get_pos()[1], s=b.get_size() * 50)

        ax.scatter(init_pos[0], init_pos[1], s=2)
        ax.arrow(init_pos[0], init_pos[1], init_vel[0], init_vel[1], fc='r', ec='r', width=0.01, head_width=1, head_length=1)

    def plot_frame(self, pos, vel, dv, t):
        if pos is None:
            return
        self._cleanup()
        self._plot_frame(pos, vel, dv, t)

    def _cleanup(self):
        for artist in self._artists:
            artist.remove()

    def _plot_frame(self, pos, vel, dv, t):
        ax = self._ax
        artists = []

        # object
        artist = ax.scatter(pos[0], pos[1], s=2)
        artist.set_zorder(19)
        artists.append(artist)

        # path
        if self._last_pos is not None:
            lp = self._last_pos
            ax.plot(np.array([lp[0], pos[0]]), np.array([lp[1], pos[1]]), c='k', lw=0.5)

        # persist
        self._artists = artists
        self._last_pos = pos

class Action(Enum):
    SHOW = 1
    HTML = 2


def animate(i, eq, plotter):
    pos, vel, dv, t = eq.process_dt( 10 )
    plotter.plot_frame(pos, vel, dv, t)


# -- setup parameters

action = Action.SHOW
name = 'Two-Bodies'
frames = None
if action == Action.HTML:
    frames = 500

bodies = []
bodies.append( Body(np.array([20, 60]), 20) )
#bodies.append( Body(np.array([60, 60]), 10) )

init_pos = np.array([40,60])
init_vel = np.array([0,-6.33])

h = 0.01
n = 5000

# -- setup

fig, ax = plt.subplots()

plotter = Plotter(ax)
plotter.setup()
fig.tight_layout()
plotter.plot_situation(init_pos, init_vel, bodies)

integ = it.RungeKutta4th( DiffEq(), init_pos, init_vel, h )

# -- run

anim = animation.FuncAnimation(fig, animate, interval=50, fargs=(integ,plotter,), blit=False, frames=frames)

if action == Action.SHOW:
    plt.show()

elif action == Action.HTML:

    print(animation.writers.list())

    Writer = animation.writers['html']
    writer = Writer(fps=15, metadata=dict(artist='Dominic Ast D!'), bitrate=1800)

    anim.save(name + '.html', writer=writer)

else:
    raise Exception('Unknown action')
