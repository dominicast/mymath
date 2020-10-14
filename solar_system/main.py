
from mayavi import mlab

import numpy as np
import time

from solver import Solver


class Logger:

    def log(self, tag, *values, level):
        pass

    def inc_level(self):
        pass

    def dec_level(self):
        pass


class Body:

    def __init__(self, m, r, sp, sv):
        self._m = m
        self._r = r
        self._sp = sp
        self._sv = sv
        self._render_color = None
        self._render_size = None
        self._render_object = None
        self._index = None

    def get_m(self):
        return self._m

    def get_r(self):
        return self._r

    def get_sp(self):
        return self._sp

    def get_sv(self):
        return self._sv

    def get_render_color(self):
        return self._render_color

    def set_render_color(self, render_color):
        self._render_color = render_color

    def get_render_size(self):
        return self._render_size

    def set_render_size(self, render_size):
        self._render_size = render_size

    @staticmethod
    def get_render_x(x):
        return x

    @staticmethod
    def get_render_y(y):
        return y

    @staticmethod
    def get_render_z(z):
        return z

    def get_render_object(self):
        return self._render_object

    def set_render_object(self, render_object):
        self._render_object = render_object

    def get_inex(self):
        return self._index

    def set_index(self, index):
        self._index = index


class SolarSystemBodyFactory:

    @staticmethod
    def create_sun():
        mass = 1.98892*pow(10,30)
        radius = 6.96342*pow(10,5)
        position = np.array([[0., 0., 0.]])
        velocity = np.array([[0., 0., 0.]])
        body = Body(m=mass, r=radius, sp=position, sv=velocity)
        size = radius
        color = (1., 0., 0.)
        body.set_render_color(color)
        body.set_render_size(size)
        return body

    @staticmethod
    def create_earth():
        mass = 5.9722*pow(10,24)
        radius = 6.371*pow(10,3)
        distance = 1.5*pow(10,8)
        velocity = 107208
        position = np.array([[distance, 0., 0.]])
        velocity = np.array([[0., 0., velocity]])
        body = Body(m=mass, r=radius, sp=position, sv=velocity)
        #size = radius
        size = 6.96342*pow(10,5)
        color = (0., 0., 1.)
        body.set_render_color(color)
        body.set_render_size(size)
        return body

    @staticmethod
    def create_bodies():

        sun = body_factory.create_sun()
        earth = body_factory.create_earth()

        bodies = [sun, earth]

        i = 0
        for body in bodies:
            body.set_index(i)
            i = i + 1

        return bodies


@mlab.animate(ui=False, delay=100)
def anim(bodies, solver, scene, speed):

    ts_save = time.time()

    yield

    while True:

        ts = time.time()

        frame_dt = (ts - ts_save) * speed

        ts_save = ts

        # ---

        pos = solver.process(frame_dt)

        # ---

        scene.disable_render = True

        for body in bodies:
            index = body.get_inex()
            x = body.get_render_x(pos[index,0])
            y = body.get_render_y(pos[index,1])
            z = body.get_render_z(pos[index,2])
            body.get_render_object().set(x=x, y=y, z=z)

        scene.disable_render = False

        yield


if __name__ == '__main__':

    body_factory = SolarSystemBodyFactory()
    bodies = body_factory.create_bodies()

    speed = 3
    dt = 0.001

    solver = Solver(bodies, dt, Logger())

    #fig = mlab.figure(size=(1000,600))
    fig = mlab.figure()
    #fig.scene.anti_aliasing_frames = 0

    for body in bodies:
        sp_sun = body.get_sp()[0]
        x = body.get_render_x(sp_sun[0])
        y = body.get_render_y(sp_sun[1])
        z = body.get_render_z(sp_sun[2])
        color = body.get_render_color()
        size = body.get_render_size()
        pts = mlab.points3d(x, y, z, color=color, scale_factor=size)
        body.set_render_object(pts.mlab_source)

    #mlab.view(0, 0, 10)
    mlab.view(0, 90, 80)

    #mlab.axes(color=(.7, .7, .7), extent=[-10, 10, -10, 10, 0, 10], xlabel='x', ylabel='y', zlabel='z')

    a = anim(bodies, solver, fig.scene, speed)

    mlab.show()
