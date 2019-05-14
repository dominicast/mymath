
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import juggle_axes
from matplotlib import animation
import numpy as np
import math
import integ as it

from scipy.optimize import fsolve


class DiffEq:

    def f(self, pos, vel, t):
        return -9.81*radius*math.sin(pos)


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


def quiver_data_to_segments(ov, v):
    len = math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2) + math.pow(v[2], 2))
    segments =(ov[0], ov[1], ov[2], ov[0]+v[0]*len, ov[1]+v[1]*len, ov[2]+v[2]*len)
    segments = np.array(segments).reshape(6, -1)
    return [[[x, y, z], [u, v, w]] for x, y, z, u, v, w in zip(*list(segments))]


def set_pendulum_pos(pos):
    global the_pendulum_mass
    global the_pendulum_line
    global the_pendulum_vel

    the_pendulum_line.set_data([mp[0], pos[0]], [mp[1], pos[1]])
    the_pendulum_line.set_3d_properties([mp[2], pos[2]])

    the_pendulum_mass.set_data(pos[0], pos[1])
    the_pendulum_mass.set_3d_properties(pos[2])

    the_pendulum_vel.set_segments(quiver_data_to_segments(pos, pos))


def animate(i):
    global the_pendulum

    off = math.radians(0.5)

    phi,vel = the_pendulum.execute(0.001, 10)

    if phi > -off and phi < off:
        return

    if phi > 0:
        r = cicle.calc_point(phi, sp)
    else:
        phi = -phi
        r = cicle.calc_point(phi, sp)
        r[0] = -r[0]
        r[1] = -r[1]

    new_pendulum_pos = mp + r

    set_pendulum_pos(new_pendulum_pos)


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

    # -- show

    global the_pendulum
    global the_pendulum_mass
    global the_pendulum_line
    global the_pendulum_vel

    the_pendulum_mass, = ax.plot([], [], [], "o", markersize=5)

    the_pendulum_line, = ax.plot([], [], [], lw=0.5)

    the_pendulum_vel = ax.quiver([], [], [], [], [], [])

    set_pendulum_pos(sp)

    the_pendulum = it.RungeKutta4th(DiffEq(), alpha, 0)

    anim = animation.FuncAnimation(fig, animate, interval=10, blit=False)

    plt.show()
