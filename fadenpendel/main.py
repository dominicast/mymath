
from utils import *

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import juggle_axes
from matplotlib import animation
import numpy as np
import math
import integ as it


class DiffEq:

    def __init__(self, radius):
        self._radius = radius

    def f(self, pos, vel, t):
        return -(9.81/self._radius)*math.sin(pos)


def animate(i, integ_ctx, plot_ctx):

    rho,vel = integ_ctx.get_deq().execute(integ_ctx.get_dt(), integ_ctx.get_count())

    # ---

    pos = plot_ctx.get_circle().calc(rho)

    mp_l = plot_ctx.get_mp()

    rr = mp_l - pos

    # velocity

    z = pos[2]
    x = -(rr[2]*z/(rr[0]+rr[1]*(pos[1]/pos[0])))
    y = (pos[1]/pos[0])*x

    vv = np.array([x, y, z])

    if rho < 0:
        vv = vv * (-1)

    len = math.sqrt(math.pow(vv[0],2)+math.pow(vv[1],2)+math.pow(vv[2],2))

    vv = vv / len * vel * radius

    # ---

    ax_l = plot_ctx.get_ax()

    #global the_pendulum_acc

    # line plot

    actor = plot_ctx.get_line()

    if actor is None:
        actor, = ax.plot([], [], [], lw=0.5)
        plot_ctx.set_line(actor)

    actor.set_data([mp_l[0], pos[0]], [mp_l[1], pos[1]])
    actor.set_3d_properties([mp_l[2], pos[2]])

    # mass plot

    actor = plot_ctx.get_mass()

    if actor is None:
        actor, = ax.plot([], [], [], "o", markersize=5)
        plot_ctx.set_mass(actor)

    actor.set_data(pos[0], pos[1])
    actor.set_3d_properties(pos[2])

    # rr plot

    #if plot_ctx.get_rr() is not None:
    #    plot_ctx.get_rr().remove()

    #actor = ax_l.quiver(pos[0], pos[1], pos[2], rr[0], rr[1], rr[2])

    #plot_ctx.set_rr(actor)

    # velocity

    if plot_ctx.get_vel() is not None:
        plot_ctx.get_vel().remove()

    actor = ax_l.quiver(pos[0], pos[1], pos[2], vv[0], vv[1], vv[2])

    plot_ctx.set_vel(actor)


if __name__ == '__main__':

    radius = 1

    rho_max = math.radians(40)

    phi = math.radians(0)

    time_factor = 1

    # -- integration

    deq = it.RungeKutta4th(DiffEq(radius), rho_max, 0)

    integ_dt = 0.01    # [s]
    integ_count = 10
    integ_freq = 100   # [ms]

    if integ_dt * integ_count * 1000 != integ_freq:
        print('Invalid time configuration')

    integ_count = round(integ_count * time_factor)

    integ_ctx = IntegrationCtx(deq, integ_dt, integ_count)

    # -- define initial situation

    # mount point
    mp = np.array([0, 0, radius+(radius/10)])

    # representing the circle of the pendulum
    circle = Circle(radius, mp, phi)

    # -- setup plot

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.set_xlabel('x', fontsize=15)
    ax.set_xlim3d(-radius, radius)

    ax.set_ylabel('y', fontsize=15)
    ax.set_ylim3d(-radius, radius)

    ax.set_zlabel('z', fontsize=15)
    ax.set_zlim3d(0, radius+2*(radius/10))

    # -- plot initial situation

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

    # -- show

    plot_ctx = PlotCtx(ax, mp, circle)

    anim = animation.FuncAnimation(fig, animate, interval=integ_freq, fargs=(integ_ctx,plot_ctx,), blit=False)

    plt.show()
