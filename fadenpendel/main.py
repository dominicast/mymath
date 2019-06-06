
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


if __name__ == '__main__':

    config = Config()

    radius = config.get_radius()
    rho_max = config.get_rho_max()
    time_factor = config.get_time_factor()

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

    # -- integration

    integ_dt = config.get_integ_dt()
    integ_count = config.get_integ_count()
    integ_freq = config.get_integ_freq()

    if integ_dt * integ_count * 1000 != integ_freq:
        print('Invalid time configuration')

    integ_count = round(integ_count * time_factor)

    # -- pendulum

    friction = config.get_friction()

    if config.get_impl() == Impl.ANGLE_INTEG:
        pendulum = PendulumAngleInteg(mp, circle, m, g, friction, integ_dt, integ_count)
        pendulum.init_deq(rho_max)
    elif config.get_impl() == Impl.FORCE_INTEG:
        pendulum = PendulumForceInteg(mp, m, g, friction, integ_dt, integ_count)
        pendulum.init_deq(circle.calc(rho_max), np.array([0, 0, 0]))
    else:
        raise Exception('Unknown implementation')

    # -- run

    anim = animation.FuncAnimation(fig, animate, interval=integ_freq, fargs=(pendulum,plotter,), blit=False)

    plt.show()
