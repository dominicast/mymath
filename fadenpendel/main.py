
from utils import *
from angle import AngleImpl
from force import ForceImpl
from config import *

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import juggle_axes
from matplotlib import animation
import numpy as np
import math


def animate(i, integ_ctx, plot_ctx, impl):
    frame = impl.create_frame(integ_ctx, plot_ctx)
    frame.perform()


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
        impl = ForceImpl(mp, sp, plot_ctx)
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
