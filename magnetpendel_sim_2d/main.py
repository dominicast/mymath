import math
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
import integ as it
import enum

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

class SourceType:
    LINEAR = 1
    INV_SQR = 2

class Source:

    def __init__(self, rad, theta, mult, size, type):
        self._rad = rad
        self._theta = theta
        self._mult = mult
        self._size = size
        self._type = type

    def set_pos(self, pos):
        self._pos = pos

    def get_pos(self):
        return self._pos

    def get_rad(self):
        return self._rad

    def get_theta(self):
        return self._theta

    def get_mult(self):
        return self._mult

    def get_size(self):
        return self._size

    def get_type(self):
        return self._type

class DiffEq:

    def f( self, pos, vel, t, n ):

        result = np.array([0,0])

        closest_dist = None
        closest_src = None

        for src in sources:

            r = pos - src.get_pos()

            #ax.arrow(pos[0], pos[1], r[0], r[1], fc='b', ec='b', width=0.01, head_width=1, head_length=1, alpha=.05)

            dist = math.sqrt( math.pow( r[0], 2 ) + math.pow( r[1], 2 ) + math.pow( m_fHeight, 2 ) )

            if ( ( closest_dist == None ) or ( dist < closest_dist ) ):
                closest_src = src
                closest_dist = dist

            if src.get_type() == SourceType.LINEAR:
                force = src.get_mult() * r
            elif src.get_type() == SourceType.INV_SQR:
                force = (src.get_mult() / math.pow(dist, 3)) * r
            else:
                raise Exception( "Invalid source type " + repr( src.get_type() ) )

            result = result - force

            #ax.arrow(pos[0], pos[1], result[0], result[1], fc='b', ec='b', width=0.01, head_width=1, head_length=1, alpha=.5)

            #if ( ( n > m_nMinSteps ) and ( la.norm(r) < src.get_size() ) and ( la.norm(r) < m_fAbortVel ) ):

        result = result - vel * m_fFriction

        return result

class Observer:

    def notify(self, pos_n, vel_n, t_n):
        ax.scatter(pos_n[0], pos_n[1], s=2)

# -- setup parameters

m_fHeight = 10
m_fFriction = 0.0005

m_nMinSteps = 1000
m_nMaxSteps = 200
m_fAbortVel = 0.04

m_fSimWidth = 2000
m_fSimHeight = 2000

sources = []

#

# pendulum force
sources.append( Source( 0, 0, 0.000005, 1, SourceType.LINEAR ) )

# magnets
sources.append( Source( 170, 90, 10, 10, SourceType.INV_SQR ) )
sources.append( Source( 170, 210, 10, 10, SourceType.INV_SQR ) )
sources.append( Source( 170, 330, 10, 10, SourceType.INV_SQR ) )

for src in sources:
    x = m_fSimWidth / 2 + src.get_rad() * math.cos( src.get_theta() * ( math.pi / 180 ) )
    y = m_fSimHeight / 2 + src.get_rad() * math.sin( src.get_theta() * ( math.pi / 180 ) )
    pos = np.array([x, y])
    src.set_pos( pos )

init_pos = np.array([1100,500])
init_vel = np.array([0,0])

h = 2
n = 5000

#trace = False

# -- setup plot

fig, ax = plt.subplots()

ax.set_title('Magnetpendel Path')

ax.set_xlabel('x', fontsize=15)
ax.set_xlim(0, m_fSimWidth)

ax.set_ylabel('y', fontsize=15)
ax.set_ylim(0, m_fSimHeight)

ax.grid(True)
fig.tight_layout()

# -- plot initial situation

for src in sources:
    ax.scatter( src.get_pos()[0], src.get_pos()[1], s=src.get_size()*50)

ax.scatter(init_pos[0], init_pos[1], s=2)
ax.arrow(init_pos[0], init_pos[1], init_vel[0], init_vel[1], fc='r', ec='r', width=0.01, head_width=1, head_length=1)

# -- simulate equation

integ = it.Beeman( DiffEq(), init_pos, init_vel )
integ.execute( h, n, observer=Observer() )

# -- display plot

plt.show()
