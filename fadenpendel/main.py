from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import juggle_axes
from matplotlib import animation
import numpy as np
import math
import integ as it
import sys
import array
from datetime import datetime

from scipy.optimize import fsolve


class DiffEq:

    def f(self, pos, vel, t):
        return -9.81*radius*math.sin(pos)


class PathObserver():

    def __init__(self):
        self._off = math.radians(0.5)

    def notify(self, pos, vel, t, n):

        if pos > -self._off and pos < self._off:
            return

        if pos > 0:
            r = cicle.calc_point(pos, sp)
        else:
            pos = -pos
            r = cicle.calc_point(pos, sp)
            r[0] = -r[0]

        ax.quiver(mp[0], mp[1], mp[2], r[0], r[1], r[2])


class ZAxisCircle:

    def __init__(self, radius, angle):
        self._radius = radius
        self._angle = angle
        self._alpha = None

    def _equations(self, p):

        # Coordinate representation of the plain
        # through the starting point
        # and the z-axis
        b = 100
        a = -(sp[1] / sp[0]) * b
        c = 0
        d = 0

        # Vector pointing down the z-axis
        z_x = 0
        z_y = 0
        z_z = -1
        z_len = 1

        p_x, p_y, p_z = p
        p_len = math.sqrt(math.pow(p_x, 2) + math.pow(p_y, 2) + math.pow(p_z, 2))

        # Point must be on the plain
        # ax + by + cz = d
        e1 = a*p_x + b*p_y + c*p_z - d
        # Length of the vector must match the radius
        # abs(vec(x)) = radius
        e2 = p_len - self._radius
        # The angle to the z-axis must match
        # cos^-1((vec(z)*vec(p))/(abs(vec(z))*abs(vec(p)))) = angle
        e3 = math.acos((z_x*p_x + z_y*p_y + z_z*p_z) / (p_len * z_len)) - self._alpha

        return e1, e2, e3

    def process(self, starting_point, step_size, observer):
        one_degree = (math.pi / 180)
        self._alpha = self._angle
        sp = starting_point
        stack = []
        while self._alpha > 0:
            x, y, z = fsolve(self._equations, (sp[0], sp[1], sp[2]))
            if observer is not None:
                observer.notify(x, y, z)
            sp = np.array([x, y, z])
            stack.append(np.array([-x, -y, z]))
            self._alpha -= step_size * one_degree
        while len(stack) >= 1:
            sp = stack.pop()
            if observer is not None:
                observer.notify(sp[0], sp[1], sp[2])

    def calc_point(self, alpha, starting_point):
        self._alpha = alpha
        sp = starting_point
        x, y, z = fsolve(self._equations, (sp[0], sp[1], sp[2]))
        return np.array([x, y, z])


class ZAxisCirclePlotter:

    def __init__(self, local_vecor):
        self._local_vecor = local_vecor
        self._point_save = None

    def notify(self, x, y, z):

        pn = self._local_vecor + np.array([x, y, z])

        if self._point_save is None:
            self._point_save = pn
            return

        pp = self._point_save

        ax.plot(np.array([pp[0], pn[0]]), np.array([pp[1], pn[1]]), np.array([pp[2], pn[2]]), c='k', lw=0.5)

        self._point_save = pn


def set_pendulum_pos(pos):
    global the_pendulum_mass

    the_pendulum_mass.set_data(pos[0], pos[1])
    the_pendulum_mass.set_3d_properties(pos[2])


def animate(i):
    global the_pendulum

    pos,vel = the_pendulum.execute(0.0001, 200)

    print(pos)

    #set_pendulum_pos(pos)

    #print(repr(i)+' : '+repr(datetime.now().microsecond/1000))
    #global lala_n
    #sct.set_data(lala_n, 0)
    #sct.set_3d_properties(70)
    #lala_n -= 1


if __name__ == '__main__':

    # -- setup plot

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.set_xlabel('x', fontsize=15)
    ax.set_xlim3d(-30, 30)

    ax.set_ylabel('y', fontsize=15)
    ax.set_ylim3d(-30, 30)

    ax.set_zlabel('z', fontsize=15)
    ax.set_zlim3d(50, 100)

    # -- define initial situation

    # mount point
    mp = np.array([0, 0, 100])

    # starting point
    sp = np.array([20, 0, 60])

    sr = sp - mp

    radius = math.sqrt(math.pow(sr[0], 2) + math.pow(sr[1], 2) + math.pow(sr[2], 2))
    alpha = math.acos((0*sr[0] + 0*sr[1] + (-1)*sr[2]) / (1 * radius))

    cicle = ZAxisCircle(radius, alpha)

    #print(radius)
    #print(alpha*180/math.pi)

    # -- plot initial situation

    # vertical line
    ax.plot(np.array([0, mp[0]]), np.array([0, mp[1]]), np.array([0, mp[2]]), c='k', lw=0.5)

    # mount point
    ax.scatter(mp[0], mp[1], mp[2], c='r')

    # expected circle
    cicle.process(sp, 5, ZAxisCirclePlotter(mp))

    # -- plot a point on the path

    #sr = cicle.calc_point(math.radians(20), sp)
    #sp = mp + sr

    # starting point
    #lala = ax.scatter(mp[0]+sr[0], mp[1]+sr[1], mp[2]+sr[2], c='b', animated=True)

    # sr vector
    #ax.quiver(mp[0], mp[1], mp[2], sr[0], sr[1], sr[2])

    # -- process

    #integ = it.SIEuler(DiffEq(), alpha, 0)
    #obs = PathObserver()
    #integ.execute(0.01, 300, observer=obs)

    # -- show

    global the_pendulum
    global the_pendulum_mass

    the_pendulum_mass, = ax.plot([], [], [], "o", markersize=5)

    set_pendulum_pos(sp)

    the_pendulum = it.Beeman(DiffEq(), alpha, 0)

    anim = animation.FuncAnimation(fig, animate, interval=200, blit=False)

    plt.show()
