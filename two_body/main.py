
from mayavi import mlab

import numpy as np
import time

from solver1 import Solver1
from solver2 import Solver2
from solver3 import Solver3


class Body:

    def __init__(self, m, sp, sv, color):
        self._m = m
        self._sp = sp
        self._sv = sv
        self._color = color
        self._mlab_source = None

    def get_m(self):
        return self._m

    def get_sp(self):
        return self._sp

    def get_sv(self):
        return self._sv

    def get_color(self):
        return self._color

    def set_mlab_source(self, mlab_source):
        self._mlab_source = mlab_source

    def get_mlab_source(self):
        return self._mlab_source


def create_solver(tag, u, v, G, dt):
    if tag == 's1':
        return Solver1(u, v, G, dt)
    elif tag == 's2':
        return Solver2(u, v, G, dt)
    elif tag == 's3':
        return Solver3(u, v, G, dt)
    else:
        raise Exception('No solver for '+repr(tag))


@mlab.animate(ui=False, delay=100)
def anim(u, v, solver, scene, speed):

    ts_save = time.time()

    yield

    while True:

        ts = time.time()

        frame_dt = (ts - ts_save) * speed

        ts_save = ts

        # ---

        pos = solver.execute(frame_dt)

        # ---

        scene.disable_render = True

        u.get_mlab_source().set(x=pos[0,0], y=pos[0,1], z=pos[0,2])
        v.get_mlab_source().set(x=pos[1,0], y=pos[1,1], z=pos[1,2])

        scene.disable_render = False

        yield


if __name__ == '__main__':

    u = Body(m=1, sp=np.array([[1., 1., 1.]]), sv=np.array([[0., 0., 0.]]), color=(1., 0., 0.))
    v = Body(m=1, sp=np.array([[0., 0., 0.]]), sv=np.array([[0., 1., 0.]]), color=(0., 0., 1.))

    G = 1
    speed = 3
    dt = 0.001

    # ---

    solver = create_solver('s1', u, v, G, dt)

    # ---

    fig = mlab.figure()
    #fig.scene.anti_aliasing_frames = 0

    sp_u = u.get_sp()[0]
    pts = mlab.points3d(sp_u[0], sp_u[1], sp_u[2], color=u.get_color(), scale_factor=u.get_m())
    u.set_mlab_source(pts.mlab_source)

    sp_v = v.get_sp()[0]
    pts = mlab.points3d(sp_v[0], sp_v[1], sp_v[2], color=v.get_color(), scale_factor=v.get_m())
    v.set_mlab_source(pts.mlab_source)

    mlab.view(0, 90, 80)

    #mlab.axes(color=(.7, .7, .7), extent=[-10, 10, -10, 10, 0, 10], xlabel='x', ylabel='y', zlabel='z')

    a = anim(u, v, solver, fig.scene, speed)

    mlab.show()
