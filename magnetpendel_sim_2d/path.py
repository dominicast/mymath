import matplotlib.pyplot as plt
import integ as it
from config.triangle import *
from mp.eq import DiffEq
from mp.observer import Observer
import numpy as np
from matplotlib import animation
from multiprocessing import Process, Queue, Event
import time
from enum import Enum


# Display path from init_pos with velocity init_vel
# to one of the magnets


class PointType(Enum):
    PATH = 1
    END = 2


class Point:

    def __init__(self, pos, type, color):
        self._pos = pos
        self._type = type
        self._color = color

    def get_pos(self):
        return self._pos

    def get_type(self):
        return self._type

    def get_color(self):
        return self._color


class PathObserver(Observer):

    def __init__(self, cfg, color, q, e):
        super().__init__(cfg)
        self._color = color
        self._q = q
        self._e = e

    def _step_done(self, pos, n):
        if self._e.is_set():
            return True
        if n % self._cfg.m_nProbeModulo == 0:
            self._q.put(Point(pos, PointType.PATH, self._color))
            time.sleep(0.005)

    def _process_done(self, pos, n, found):
        if found:
            self._q.put(Point(pos, PointType.END, self._color))


class InitialValue:

    def __init__(self, pos, vel, color, q):
        self._pos = pos
        self._vel = vel
        self._color = color
        self._q = q
        self._last_pos = None

    def get_pos(self):
        return self._pos

    def get_vel(self):
        return self._vel

    def get_color(self):
        return self._color

    def get_q(self):
        return self._q

    def get_last_pos(self):
        return self._last_pos

    def set_last_pos(self, last_pos):
        self._last_pos = last_pos


def worker(w_init_pos, w_init_vel, w_cfg, color, q, e):
    integ = it.RungeKutta4th(DiffEq(cfg), w_init_pos, w_init_vel)
    obs = PathObserver(w_cfg, color, q, e)
    integ.execute(cfg.m_fTimeStep, cfg.m_nMaxSteps, observer=obs)


def animate(i):
    for init_value in init_values:
        q = init_value.get_q()
        while not q.empty():
            point = q.get()
            pos = point.get_pos()
            if point.get_type() == PointType.END:
                ax.scatter(pos[0], pos[1], c="y", s=140, marker="x", zorder=100)
            else:
                if init_value.get_last_pos() is not None:
                    lp = init_value.get_last_pos()
                    ax.plot(np.array([lp[0], pos[0]]), np.array([lp[1], pos[1]]), c=point.get_color(), lw=0.5)
                init_value.set_last_pos(pos)


if __name__ == '__main__':

    cfg = TriangleConfig()

    init_values = [
        #InitialValue(np.array([200, 600]), np.array([0, 0]), 'r', Queue()),
        InitialValue(np.array([800, 800]), np.array([0, 0]), 'k', Queue())
        #InitialValue(np.array([100, 100]), np.array([0, 0]), 'k', Queue())
    ]

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

    for init_value in init_values:
        p = init_value.get_pos()
        ax.scatter(p[0], p[1], c=init_value.get_color(), s=30)
    #ax.arrow(init_pos[0], init_pos[1], init_vel[0], init_vel[1], fc='r', ec='r', width=0.01, head_width=1, head_length=1)

    # -- simulate equation

    terminate_event = Event()

    processes = []
    for init_value in init_values:
        process = Process(target=worker, args=(init_value.get_pos(), init_value.get_vel(), cfg, init_value.get_color(), init_value.get_q(), terminate_event))
        process.start()
        processes.append(process)

    anim = animation.FuncAnimation(fig, animate, interval=100)

    plt.show()

    terminate_event.set()

    for process in processes:
        process.join()
