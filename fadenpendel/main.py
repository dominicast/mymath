
from utils import *
from plotter import *
from angle import AngleImpl
from force import ForceImpl
from config import *

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import juggle_axes
from matplotlib import animation
import numpy as np


def animate(i, integ_ctx, plotter, impl):
    frame = impl.create_frame(integ_ctx)
    data = frame.perform()
    plotter.plot_frame(data)


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

    plotter = Plotter(ax, mp)
    plotter.setup(radius)
    plotter.plot_situation(circle, rho_max)

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

    # -- run

    anim = animation.FuncAnimation(fig, animate, interval=integ_freq, fargs=(integ_ctx,plotter,impl,), blit=False)

    plt.show()
