
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import juggle_axes
from matplotlib import animation
import numpy as np
import math
import integ as it


class DiffEq:

    def f(self, pos, vel, t):
        return -9.81*radius*math.sin(pos)


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


class PathPlotter:

    def __init__(self, circle, max_angle):
        self._circle = circle
        self._max_angle = max_angle
        self._point_save = None

    def plot(self, x, y, z):

        pn = np.array([x, y, z])

        if self._point_save is None:
            self._point_save = pn
            return

        pp = self._point_save

        ax.plot(np.array([pp[0], pn[0]]), np.array([pp[1], pn[1]]), np.array([pp[2], pn[2]]), c='k', lw=0.5)

        self._point_save = pn

    def process(self, step_size):
        angle = self._max_angle

        while angle >= -(self._max_angle+math.pi/1000):
            p = self._circle.calc(angle)
            self.plot(p[0], p[1], p[2])
            angle -= math.radians(step_size)


def animate(i):
    global the_pendulum

    phi,vel = the_pendulum.execute(0.01, 10)

    pos = cicle.calc(phi)

    # ---

    global the_pendulum_mass
    global the_pendulum_line
    #global the_pendulum_vel
    #global the_pendulum_acc
    #global the_pendulum_rr

    # line
    the_pendulum_line.set_data([mp[0], pos[0]], [mp[1], pos[1]])
    the_pendulum_line.set_3d_properties([mp[2], pos[2]])

    # mass
    the_pendulum_mass.set_data(pos[0], pos[1])
    the_pendulum_mass.set_3d_properties(pos[2])

    # velocity

    #if the_pendulum_vel is not None:
    #    the_pendulum_vel.remove()

    #z = pos[2]
    #x = -(rr[2]*z/(rr[0]+rr[1]*(sp[1]/sp[0])))
    #y = (sp[1]/sp[0])*x

    #vv = np.array([x, y, z])

    #if phi < 0:
    #    vv = vv * (-1)

    #len = math.sqrt(math.pow(vv[0],2)+math.pow(vv[1],2)+math.pow(vv[2],2))

    #vv = vv / len * vel * radius

    #the_pendulum_vel = ax.quiver(pos[0], pos[1], pos[2], vv[0], vv[1], vv[2])
    #the_pendulum_vel.set_segments(quiver_data_to_segments(mp, vv))

    # rr

    #if the_pendulum_rr is not None:
    #    the_pendulum_rr.remove()

    #the_pendulum_rr = ax.quiver(pos[0], pos[1], pos[2], rr[0], rr[1], rr[2])

    # acceleration

    #if the_pendulum_acc is not None:
    #    the_pendulum_acc.remove()

    #x = (r[1] * vv[2] - r[2] * vv[1])
    #y = (r[2] * vv[0] - r[0] * vv[2])
    #z = (r[0] * vv[1] - r[1] * vv[0])

    #acc = np.array([x, y, z])

    #the_pendulum_acc = ax.quiver(pos[0], pos[1], pos[2], acc[0], acc[1], acc[2])


if __name__ == '__main__':

    radius = 1
    phi_max = math.radians(40)

    # -- define initial situation

    # mount point
    mp = np.array([0, 0, 100])

    # representing the circle of the pendulum
    cicle = Circle(radius, mp, math.radians(0))

    # -- setup plot

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.set_xlabel('x', fontsize=15)
    ax.set_xlim3d(-1, 1)

    ax.set_ylabel('y', fontsize=15)
    ax.set_ylim3d(-1, 1)

    ax.set_zlabel('z', fontsize=15)
    ax.set_zlim3d(98.5, 100.5)

    # -- plot initial situation

    # vertical line
    ax.plot(np.array([0, mp[0]]), np.array([0, mp[1]]), np.array([mp[2]-radius, mp[2]]), c='k', lw=0.5)

    # mount point
    ax.scatter(mp[0], mp[1], mp[2], c='r')

    # expected circle
    PathPlotter(cicle, phi_max).process(5)

    # -- show

    global the_pendulum
    global the_pendulum_mass
    global the_pendulum_line
    #global the_pendulum_rr
    #global the_pendulum_vel
    #global the_pendulum_acc

    the_pendulum_mass, = ax.plot([], [], [], "o", markersize=5)

    the_pendulum_line, = ax.plot([], [], [], lw=0.5)

    #the_pendulum_rr = None

    #the_pendulum_vel = None

    #the_pendulum_acc = None

    #set_pendulum_pos(sr, 0, phi_max)

    the_pendulum = it.RungeKutta4th(DiffEq(), phi_max, 0)

    anim = animation.FuncAnimation(fig, animate, interval=100, blit=False)

    plt.show()
