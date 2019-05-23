
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


class Circle:

    def __init__(self, radius, mp, phi):
        self._radius = radius
        self._mp = mp
        self._phi = phi

    def calc(self, rho):
        # Kuegelkoordinaten

        x = radius * math.sin(rho) * math.cos(self._phi)
        y = radius * math.sin(rho) * math.sin(self._phi)
        z = radius * math.cos(rho)

        v = np.array([x, y, z])
        v[2] = -v[2]
        v = self._mp + v

        return v


class IntegrationCtx:

    def __init__(self, deq, dt, count):
        self._deq = deq
        self._dt = dt
        self._count = count

    def get_deq(self):
        return self._deq

    def get_dt(self):
        return self._dt

    def get_count(self):
        return self._count


class PlotCtx:

    def __init__(self, ax, mp, circle):
        self._ax = ax
        self._mp = mp
        self._circle = circle

    def get_ax(self):
        return self._ax

    def get_mp(self):
        return self._mp

    def get_circle(self):
        return self._circle


def animate(i, integ_ctx, plot_ctx):

    rho,vel = integ_ctx.get_deq().execute(integ_ctx.get_dt(), integ_ctx.get_count())

    pos = plot_ctx.get_circle().calc(rho)

    # ---

    ax_l = plot_ctx.get_ax()
    mp_l = plot_ctx.get_mp()

    global the_pendulum_mass
    global the_pendulum_line
    global the_pendulum_rr
    global the_pendulum_vel
    #global the_pendulum_acc

    # line
    the_pendulum_line.set_data([mp_l[0], pos[0]], [mp_l[1], pos[1]])
    the_pendulum_line.set_3d_properties([mp_l[2], pos[2]])

    # mass
    the_pendulum_mass.set_data(pos[0], pos[1])
    the_pendulum_mass.set_3d_properties(pos[2])

    # rr

    rr = mp_l - pos

    if the_pendulum_rr is not None:
        the_pendulum_rr.remove()

    the_pendulum_rr = ax_l.quiver(pos[0], pos[1], pos[2], rr[0], rr[1], rr[2])

    # velocity

    if the_pendulum_vel is not None:
        the_pendulum_vel.remove()

    z = pos[2]
    x = -(rr[2]*z/(rr[0]+rr[1]*(pos[1]/pos[0])))
    y = (pos[1]/pos[0])*x

    vv = np.array([x, y, z])

    if rho < 0:
        vv = vv * (-1)

    len = math.sqrt(math.pow(vv[0],2)+math.pow(vv[1],2)+math.pow(vv[2],2))

    vv = vv / len * vel * radius

    the_pendulum_vel = ax_l.quiver(pos[0], pos[1], pos[2], vv[0], vv[1], vv[2])

    # acceleration

    #if the_pendulum_acc is not None:
    #    the_pendulum_acc.remove()

    #x = (r[1] * vv[2] - r[2] * vv[1])
    #y = (r[2] * vv[0] - r[0] * vv[2])
    #z = (r[0] * vv[1] - r[1] * vv[0])

    #acc = np.array([x, y, z])

    #the_pendulum_acc = ax_l.quiver(pos[0], pos[1], pos[2], acc[0], acc[1], acc[2])


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

    global the_pendulum_mass
    global the_pendulum_line
    global the_pendulum_rr
    global the_pendulum_vel
    #global the_pendulum_acc

    the_pendulum_mass, = ax.plot([], [], [], "o", markersize=5)

    the_pendulum_line, = ax.plot([], [], [], lw=0.5)

    the_pendulum_rr = None

    the_pendulum_vel = None

    #the_pendulum_acc = None

    #set_pendulum_pos(sr, 0, rho_max)

    anim = animation.FuncAnimation(fig, animate, interval=integ_freq, fargs=(integ_ctx,plot_ctx,), blit=False)

    plt.show()
