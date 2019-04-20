import math
import numpy as np

# Jorge Rodriguez (14.07.2016)
# Math for Game Developers - Spaceship Orbits (Semi-Implicit Euler)
# https://www.youtube.com/watch?v=kxWBXd7ujx0
#
# Jorge Rodriguez (21.07.2016)
# Math for Game Developers - Verlet Integration
# https://www.youtube.com/watch?v=AZ8IGOHsjBk
#
# Wikipedia
# Beeman's algorithm
# https://en.wikipedia.org/wiki/Beeman%27s_algorithm#Equation

class Euler:

    def __init__( self, eq, init_pos, init_vel ):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

    def execute( self, h, n, observer=None ):

        pos_n = self._init_pos
        vel_n = self._init_vel
        t_n = 0

        if not (observer is None):
            observer.notify(pos_n, vel_n, t_n)

        for i in range(n):

            acc_n = self._eq.f(pos=pos_n, vel=vel_n, t=t_n, n=i)

            vel_o = vel_n + h * acc_n
            pos_o = pos_n + h * vel_n

            vel_n = vel_o
            pos_n = pos_o
            t_n += h

            if not ( observer is None ):
                observer.notify( pos_n, vel_n, t_n )

class SIEuler:

    def __init__( self, eq, init_pos, init_vel ):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

    def execute( self, h, n, observer=None ):

        pos_n = self._init_pos
        vel_n = self._init_vel
        t_n = 0

        if not (observer is None):
            observer.notify(pos_n, vel_n, t_n)

        for i in range(n):

            acc_n = self._eq.f(pos=pos_n, vel=vel_n, t=t_n, n=i)

            vel_o = vel_n + h * acc_n
            pos_o = pos_n + h * vel_o

            vel_n = vel_o
            pos_n = pos_o
            t_n += h

            if not ( observer is None ):
                observer.notify( pos_n, vel_n, t_n )

class Verlet:

    def __init__( self, eq, init_pos, init_vel ):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

    def execute( self, h, n, observer=None ):

        hr=(1/h)

        pos_m = self._init_pos
        vel_n = self._init_vel
        t_n = 0

        pos_n = pos_m + vel_n * h + (1/2) * self._eq.f(pos=pos_m, vel=vel_n, t=t_n, n=0) * math.pow( h, 2 )

        if not (observer is None):
            observer.notify(pos_n, vel_n, t_n)

        for i in range(n):

            vel_n = ( pos_n - pos_m ) * hr
            pos_o = 2 * pos_n - pos_m + self._eq.f(pos=pos_n, vel=vel_n, t=t_n, n=i) * math.pow( h, 2 )

            pos_m = pos_n
            pos_n = pos_o
            t_n += h

            if not (observer is None):
                observer.notify(pos_n, vel_n, t_n)

class Beeman:

    def __init__( self, eq, init_pos, init_vel ):
        self._eq = eq
        self._init_pos = init_pos
        self._init_vel = init_vel

    def execute( self, h, n, observer=None ):

        acc_m = np.array([0, 0])
        acc_n = np.array([0, 0])

        pos_n = self._init_pos
        vel_n = self._init_vel
        t_n = 0

        if not (observer is None):
            observer.notify(pos_n, vel_n, t_n)

        for i in range(n):

            pos_o = pos_n + h * vel_n + math.pow( h, 2 ) * ( (2/3) * acc_n - (1/6) * acc_m )
            acc_o = self._eq.f(pos=pos_n, vel=vel_n, t=t_n, n=i)
            vel_o = vel_n + h * ( (1/3) * acc_o + (5/6) * acc_n - (1/6) * acc_m )

            acc_m = acc_n
            acc_n = acc_o
            vel_n = vel_o
            pos_n = pos_o
            t_n += h

            if not (observer is None):
                observer.notify( pos_n, vel_n, t_n )
