import math
import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as la
import integ as it
from triangle import *

# Solved the following equation
#
# ddot(vec(x)) = sum(G*((m_{body})/(abs(vec(r))^3))*vec(r))
# vec(x): Path
# G: Universal gravitational constant ( 6.67408E-11 m^3 * kg^-1 * s^-2)
# m_{body}: Mass of the attracting body
# vec(r): Vector from current position the the attracting body
#
# http://asciimath.org/
#
# Jorge Rodriguez (14.07.2016)
# Math for Game Developers - Spaceship Orbits (Semi-Implicit Euler)
# https://www.youtube.com/watch?v=kxWBXd7ujx0


class DiffEq:

    def __init__(self, cfg):
        self._cfg = cfg

    def f(self, pos, vel, t, n):

        result = np.array([0,0])

        for src in self._cfg.sources:

            r = pos - src.get_pos()

            dist = math.sqrt( math.pow( r[0], 2 ) + math.pow( r[1], 2 ) + math.pow( self._cfg.m_fHeight, 2 ) )

            if src.get_type() == SourceType.LINEAR:
                force = src.get_mult() * r
            elif src.get_type() == SourceType.INV:
                force = (src.get_mult() / math.pow(dist, 2)) * r
            elif src.get_type() == SourceType.INV_SQR:
                force = (src.get_mult() / math.pow(dist, 3)) * r
            else:
                raise Exception( "Invalid source type " + repr( src.get_type() ) )

            result = result - force

        result = result - vel * self._cfg.m_fFriction

        return result


class Observer:

    def __init__(self, cfg):
        self._cfg = cfg
        self._closest_src = None
        self._n = 0
        self._len = 0

    def notify(self, pos, vel, t, n):

        # plot probe

        if n % self._cfg.m_nProbeModulo == 0:
            ax.scatter(pos[0], pos[1], c='k', s=0.01)

        # update _len

        norm_vel = la.norm(vel)

        self._len += norm_vel

        # check for stop condition

        if n < self._cfg.m_nMinSteps:
            return

        if norm_vel > self._cfg.m_fAbortVel:
            return

        b = False
        for src in self._cfg.sources:
            r = pos - src.get_pos()
            if la.norm(r) < src.get_size():
                b = True
                break

        if not b:
            return

        # stop condition satisfied
        # calculate some values

        self._n = n

        closest_dist = None

        for src in self._cfg.sources:

            if not src.get_is_magnet:
                continue

            r = pos - src.get_pos()

            dist = math.sqrt(math.pow(r[0], 2) + math.pow(r[1], 2) + math.pow(self._cfg.m_fHeight, 2))

            if (closest_dist is None) or (dist < closest_dist):
                closest_dist = dist
                self._closest_src = src

        return True

    def get_n(self):
        return self._n

    def get_len(self):
        return self._len

    def get_closest_src(self):
        return self._closest_src


cfg = TriangleConfig()

for src in cfg.sources:
    x = cfg.m_fSimWidth / 2 + src.get_rad() * math.cos( src.get_theta() * ( math.pi / 180 ) )
    y = cfg.m_fSimHeight / 2 + src.get_rad() * math.sin( src.get_theta() * ( math.pi / 180 ) )
    pos = np.array([x, y])
    src.set_pos( pos )

init_pos = np.array([200,600])
#init_pos = np.array([800,600])
init_vel = np.array([0,0])

h = cfg.m_fTimeStep
n = cfg.m_nMaxSteps

#trace = False

# -- setup plot

fig, ax = plt.subplots()

ax.set_title('Magnetpendel Path')

ax.set_xlabel('x', fontsize=15)
ax.set_xlim(0, cfg.m_fSimWidth)

ax.set_ylabel('y', fontsize=15)
ax.set_ylim(0, cfg.m_fSimHeight)

ax.grid(True)
fig.tight_layout()

# -- plot initial situation

for src in cfg.sources:
    if src.get_show():
        ax.scatter( src.get_pos()[0], src.get_pos()[1], c=src.get_color(), s=src.get_size()*50)

ax.scatter(init_pos[0], init_pos[1], s=2)
ax.arrow(init_pos[0], init_pos[1], init_vel[0], init_vel[1], fc='r', ec='r', width=0.01, head_width=1, head_length=1)

# -- simulate equation

#integ = it.Euler( DiffEq(cfg), init_pos, init_vel )
#integ = it.SIEuler( DiffEq(cfg), init_pos, init_vel )
#integ = it.Verlet( DiffEq(cfg), init_pos, init_vel )
#integ = it.Beeman( DiffEq(cfg), init_pos, init_vel )
integ = it.Midpoint( DiffEq(cfg), init_pos, init_vel )


obs = Observer(cfg)

integ.execute( h, n, observer=obs )

if not obs.get_closest_src() is None:
    print( obs.get_closest_src().get_color() + ' : ' + repr( obs.get_n() ) + ' : ' + repr( obs.get_len() ) )
else:
    print( 'did not end' )

# -- display plot

plt.show()
