
import integ as it

from mayavi import mlab

import numpy as np
import math
import time


class DiffEq:

    def __init__(self, G, m_u, m_v):
        self._G = G
        self._m_u = m_u
        self._m_v = m_v

    def f(self, pos, vel, t):

        G = self._G

        m_u = self._m_u
        m_v = self._m_v

        u = pos[0]
        v = pos[1]

        r = u - v
        r_len = math.sqrt(r[0]**2+r[1]**2+r[2]**2)

        factor = -G * ((m_u*m_v)/(r_len**3))

        F_v = factor * r
        F_u = factor * -r

        return np.array([F_v, F_u])


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


@mlab.animate(ui=False, delay=100)
def anim(u, v, scene, speed, dt):

    ts_save = time.time()

    yield

    while True:

        ts = time.time()

        frame_dt = (ts - ts_save) * speed

        ts_save = ts

        dt_count = round(frame_dt / dt)

        # ---

        pos, vel, _, t = deq.execute(dt, dt_count)

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
    speed = 1
    dt = 0.001

    # ---

    sp = np.concatenate((u.get_sp(), v.get_sp()), axis=0)
    sv = np.concatenate((u.get_sv(), v.get_sv()), axis=0)

    deq = it.RungeKutta4th(DiffEq(G, u.get_m(), v.get_m()), sp, sv)

    # ---

    fig = mlab.figure()
    #fig.scene.anti_aliasing_frames = 0

    sp_u = sp[0]
    pts = mlab.points3d(sp_u[0], sp_u[1], sp_u[2], color=u.get_color())
    u.set_mlab_source(pts.mlab_source)

    sp_v = sp[1]
    pts = mlab.points3d(sp_v[0], sp_v[1], sp_v[2], color=v.get_color())
    v.set_mlab_source(pts.mlab_source)

    mlab.view(0, 90, 80)

    mlab.axes(color=(.7, .7, .7), extent=[-10, 10, -10, 10, 0, 10], xlabel='x', ylabel='y', zlabel='z')

    a = anim(u, v, fig.scene, speed, dt)

    mlab.show()
