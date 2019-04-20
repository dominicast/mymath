import math
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
import integ as it

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

class Body:

    def __init__(self, pos, size):
        self._pos = pos
        self._size = size

    def get_pos(self):
        return self._pos

    def get_size(self):
        return self._size

class DiffEq:

    def f( self, pos, vel, t, n ):
        result = np.array([0,0])

        G = 0.1    # yes thats not the real value
        rexp = 1   # 3 is correct but we us 1 for convenience

        for b in bodies:

            r = b.get_pos() - pos

            if n % 5 == 0 and trace:
                ax.arrow(pos[0], pos[1], r[0], r[1], fc='y', ec='y', width=0.01, head_width=1, head_length=1, alpha=.05)

            m = b.get_size()
            rn = la.norm(r)
            rnq = math.pow( rn, rexp )

            fact = G * ( m / rnq )

            if trace:
                print( repr(m)+' : '+repr( rn )+' : '+repr( rnq )+' : '+repr( fact ) )

            result = result + fact * r

        if n % 5 == 0 and trace:
            vv = 5 * result
            ax.arrow(pos[0], pos[1], vv[0], vv[1], fc='b', ec='b', width=0.01, head_width=1, head_length=1, alpha=.05)

        return result

# class DiffEq:
#
#     def f( self, pos, vel, t, n ):
#         result = np.array([0, 0])
#         for b in bodies:
#             r = b.get_pos() - pos
#             if trace:
#                 ax.arrow(pos[0], pos[1], r[0], r[1], fc='b', ec='b', width=0.01, head_width=1, head_length=1, alpha=.05)
#             result = result +  0.1 * r
#         return result

class Observer:

    def notify(self, pos_n, vel_n, t_n):
        ax.scatter(pos_n[0], pos_n[1], s=2)

# -- setup parameters

bodies = []
bodies.append( Body(np.array([20, 60]), 20) )
#bodies.append( Body(np.array([60, 60]), 10) )

init_pos = np.array([40,60])
init_vel = np.array([0,-6.33])

h = 0.01
n = 5000

trace = False

# -- setup plot

fig, ax = plt.subplots()

ax.set_title('Path')

ax.set_xlabel('x', fontsize=15)
ax.set_xlim(0, 100)

ax.set_ylabel('y', fontsize=15)
ax.set_ylim(0, 100)

ax.grid(True)
fig.tight_layout()

# -- plot initial situation

for b in bodies:
    ax.scatter( b.get_pos()[0], b.get_pos()[1], s=b.get_size()*50)

ax.scatter(init_pos[0], init_pos[1], s=2)
ax.arrow(init_pos[0], init_pos[1], init_vel[0], init_vel[1], fc='r', ec='r', width=0.01, head_width=1, head_length=1)

# -- simulate equation

integ = it.SIEuler( DiffEq(), init_pos, init_vel )
integ.execute( h, n, observer=Observer() )

# -- display plot

plt.show()
