
from utils import *
from plotter import *
from angle import PendulumAngleInteg
from force import PendulumForceInteg
from config import *

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import juggle_axes
from matplotlib import animation
import numpy as np


def animate(i, pendulum, plotter):
    data = pendulum.calculate_frame()
    plotter.plot_frame(data)


# by Dominic Ast D! dominic_ast@gmx.ch
if __name__ == '__main__':

    config = NoFrictionConfig().get_config(Impl.FORCE_INTEG, Action.SHOW)

    radius = config.get_radius()
    rho_max = config.get_rho_max()

    m = config.get_m()
    g = config.get_g()

    # -- situation

    # mount point
    mp = np.array([0, 0, radius+(radius/10)])

    # circle
    circle = Circle(radius, mp, config.get_phi())

    # -- setup plot

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    plotter = Plotter(ax, mp)
    plotter.setup(radius)
    plotter.plot_situation(circle, rho_max)

    # -- pendulum

    friction = config.get_friction()
    dt = config.get_dt()
    speed = config.get_speed()

    if config.get_impl() == Impl.ANGLE_INTEG:
        pendulum = PendulumAngleInteg(mp, circle, m, g, friction, speed)
        pendulum.init_deq(rho_max, dt)
    elif config.get_impl() == Impl.FORCE_INTEG:
        pendulum = PendulumForceInteg(mp, m, g, friction, speed)
        pendulum.init_deq(circle.calc(rho_max), np.array([0, 0, 0]), dt)
    else:
        raise Exception('Unknown implementation')

    # -- run

    anim = animation.FuncAnimation(fig, animate, interval=config.get_interval(), fargs=(pendulum,plotter,), blit=False, frames=config.get_frames())

    if config.get_action() == Action.SHOW:
        plt.show()

    elif config.get_action() == Action.HTML:

        print(animation.writers.list())

        Writer = animation.writers['html']
        writer = Writer(fps=15, metadata=dict(artist='Dominic Ast D!'), bitrate=1800)

        anim.save(config.get_name()+'.html', writer=writer)

    else:
        raise Exception('Unknown action')
