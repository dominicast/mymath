import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt

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
#
# Jorge Rodriguez (21.07.2016)
# Math for Game Developers - Verlet Integration
# https://www.youtube.com/watch?v=AZ8IGOHsjBk

class Euler:

    def __init__( self, eq, init_pos, init_vel ):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

    def execute( self, h, n, observer=None ):

        pos_n = self._init_pos
        vel_n = self._init_vel

        for i in range(n):

            if not ( observer is None ):
                observer.notify( pos_n, vel_n )

            acc_n = self._eq.f(pos_n, vel_n)

            vel_o = vel_n + h * acc_n
            pos_o = pos_n + h * vel_n

            vel_n = vel_o
            pos_n = pos_o

class EulerSemiImplicit:

    def __init__( self, eq, init_pos, init_vel ):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

    def execute( self, h, n, observer=None ):

        pos_n = self._init_pos
        vel_n = self._init_vel

        for i in range(n):

            if not ( observer is None ):
                observer.notify( pos_n, vel_n )

            acc_n = self._eq.f(pos_n, vel_n, i)

            vel_o = vel_n + h * acc_n
            pos_o = pos_n + h * vel_o

            vel_n = vel_o
            pos_n = pos_o

class Body:

    def __init__(self, pos, size):
        self._pos = pos
        self._size = size

    def get_pos(self):
        return self._pos

    def get_size(self):
        return self._size

class DiffEq:

    def f( self, pos, vel, n ):
        result = np.array([0,0])

        G = 0.1

        for b in bodies:

            r = b.get_pos() - pos

            if n % 5 == 0 and trace:
                ax.arrow(pos[0], pos[1], r[0], r[1], fc='y', ec='y', width=0.01, head_width=1, head_length=1, alpha=.05)

            m = b.get_size()
            rn = la.norm(r)

            #rnq = math.pow( rn, 3 )
            rnq = rn

            fact = G * ( m / rnq )

            if trace:
                print( repr(m)+' : '+repr( rn )+' : '+repr( rnq )+' : '+repr( fact ) )

            result = result + fact * r

        if n % 5 == 0 and trace:
            vv = 5 * result
            ax.arrow(pos[0], pos[1], vv[0], vv[1], fc='b', ec='b', width=0.01, head_width=1, head_length=1, alpha=.05)

        return result

class Observer:

    def notify(self, pos_n, vel_n):
        ax.scatter(pos_n[0], pos_n[1], s=2)


# -- setup parameters

bodies = []
bodies.append( Body(np.array([20, 60]), 10) )
bodies.append( Body(np.array([60, 60]), 10) )

init_pos = np.array([40,60])
init_vel = np.array([-1,-10])

h = 0.1
n = 400

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

integ = EulerSemiImplicit( DiffEq(), init_pos, init_vel )
integ.execute( h, n, Observer() )

# -- display plot

plt.show()












#path = np.array([ [init_pos[0],init_pos[1]] ])

#xy = np.array([[1,1], [2,2], [3,3]])

#path = np.array([[]])
#path.shape = (1,2)
#np.append(path, pos_n, axis=0)
#e = np.array([1,1])
#e.shape = (1,2)
#xy = np.append(xy, e, axis=0)
#xy = np.array([1,1])
#xy.shape = (2,1)
#path = np.transpose(start_pos)
#path = np.array(start_pos)
#path = np.append(r, np.array([[5,5]]), axis=0)

# ---


#ax.scatter(delta1[:-1], delta1[1:], c=close, s=volume, alpha=0.5)
#ax.scatter(path[:,0], path[:,1], s=2)


