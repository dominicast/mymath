
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import juggle_axes
from matplotlib import animation
import numpy as np
import math
import integ as it

#import datetime
#import time

import sys

from scipy.optimize import fsolve


#The ode
class DiffEq:

    def f(self, pos, vel, t):
        return -9.81*radius*math.sin(pos)


# Circle of radius r on the plain defined by
# the z-axis and the plain-point pp
# calculating the radius vactors
class Circle:

    def __init__(self, r, pp):
        self._r = r
        self._pp = pp  # any point on the plain
        self._sp = self.calc(math.pi/4, np.array([r/2, r/2, r/2]))
        print(self._sp)
        zz = mp+self._sp
        #ax.scatter(zz[0], zz[1], zz[2], c='r')
        self._phi = None

    def _equations(self, p):

        # Coordinate representation of the plain
        # through the starting point
        # and the z-axis
        #b = 100
        b = 1
        a = -(self._pp[1] / self._pp[0]) * b
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
        e2 = p_len - self._r
        # The angle to the z-axis must match
        # cos^-1((vec(z)*vec(p))/(abs(vec(z))*abs(vec(p)))) = angle
        e3 = math.acos((z_x*p_x + z_y*p_y + z_z*p_z) / (p_len * z_len)) - self._phi

        return e1, e2, e3

    def calc(self, angle, starting_point):
        self._phi = angle
        sp = starting_point
        x, y, z = fsolve(self._equations, (sp[0], sp[1], sp[2]))
        self._phi = None
        return np.array([x, y, z])


# Plots the path of the pendulum
# mounted at mount point mp
# with circle circle
#
class PathPlotter:

    def __init__(self, mp, circle, phi_max):
        self._mp = mp
        self._circle = circle
        self._phi_max = phi_max
        self._point_save = None

    def plot(self, x, y, z):

        pn = self._mp + np.array([x, y, z])

        if self._point_save is None:
            self._point_save = pn
            return

        pp = self._point_save

        ax.plot(np.array([pp[0], pn[0]]), np.array([pp[1], pn[1]]), np.array([pp[2], pn[2]]), c='k', lw=0.5)

        self._point_save = pn

    def process(self, starting_point, step_size):
        one_degree = (math.pi / 180)
        phi = self._phi_max
        sp = starting_point
        stack = []

        while phi > 0:
            p = self._circle.calc(phi, sp)
            self.plot(p[0], p[1], p[2])
            sp = np.array([p[0], p[1], p[2]])
            stack.append(np.array([-p[0], -p[1], p[2]]))
            phi -= step_size * one_degree

        while len(stack) >= 1:
            sp = stack.pop()
            self.plot(sp[0], sp[1], sp[2])


# ---
def quiver_data_to_segments(ov, v):
    len = math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2) + math.pow(v[2], 2))
    segments =(ov[0], ov[1], ov[2], ov[0]+v[0]*len, ov[1]+v[1]*len, ov[2]+v[2]*len)
    segments = np.array(segments).reshape(6, -1)
    return [[[x, y, z], [u, v, w]] for x, y, z, u, v, w in zip(*list(segments))]


# ---
def set_pendulum_pos(r, vel, phi):
    global the_pendulum_mass
    global the_pendulum_line
    #global the_pendulum_vel
    #global the_pendulum_acc
    #global the_pendulum_rr

    pos = mp + r
    #rr = -r

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


# ---
def animate(i):
    global the_pendulum

    off = math.radians(2)

    #start = time.time()

    phi,vel = the_pendulum.execute(0.01, 10)

    if phi > -off and phi < off:
        return

    if phi > 0:
        r = cicle.calc(phi, sp)
    else:
        r = cicle.calc(-phi, sp)
        r[0] = -r[0]
        r[1] = -r[1]

    set_pendulum_pos(r, vel, phi)

    #print(time.time() - start)


if __name__ == '__main__':

    radius = 1
    phi_max = math.radians(30)

    # -- setup plot

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.set_xlabel('x', fontsize=15)
    ax.set_xlim3d(-1, 1)

    ax.set_ylabel('y', fontsize=15)
    ax.set_ylim3d(-1, 1)

    ax.set_zlabel('z', fontsize=15)
    ax.set_zlim3d(98.5, 100.5)

    # -- define initial situation

    # mount point
    mp = np.array([0, 0, 100])

    # representing the circle of the pendulum
    cicle = Circle(radius, np.array([radius, mp[1], mp[2]]))

    # starting point
    #sp = cicle.calc(phi_max, np.array([radius, mp[1], mp[2]]))

    # starting radius
    #sr = mp + sp

    # -- plot initial situation

    # vertical line
    ax.plot(np.array([0, mp[0]]), np.array([0, mp[1]]), np.array([mp[2]-radius, mp[2]]), c='k', lw=0.5)

    # mount point
    ax.scatter(mp[0], mp[1], mp[2], c='r')

    # expected circle
    #PathPlotter(mp, cicle, phi_max).process(sp, 5)




    # starting point
    #ax.scatter(sp[0], sp[1], sp[2], c='b')





















    # -- plot a point on the path

    #sr = cicle.calc(math.radians(20), sp)
    #sp = mp + sr

    # sr vector
    #ax.quiver(mp[0], mp[1], mp[2], sr[0], sr[1], sr[2])

    # -- show

    #global the_pendulum
    #global the_pendulum_mass
    #global the_pendulum_line
    #global the_pendulum_rr
    #global the_pendulum_vel
    #global the_pendulum_acc

    #the_pendulum_mass, = ax.plot([], [], [], "o", markersize=5)

    #the_pendulum_line, = ax.plot([], [], [], lw=0.5)

    #the_pendulum_rr = None

    #the_pendulum_vel = None

    #the_pendulum_acc = None

    #set_pendulum_pos(sr, 0, phi_max)

    #the_pendulum = it.RungeKutta4th(DiffEq(), phi_max, 0)

    #anim = animation.FuncAnimation(fig, animate, interval=100, blit=False)

    plt.show()
