import matplotlib.pyplot as plt
from matplotlib import animation
import integ as it
from config.triangle import *
from mp.eq import DiffEq
from mp.observer import Observer
import numpy as np
from multiprocessing import Process, Queue, Event


# Display path from init_pos with velocity init_vel
# to one of the magnets


class Point:

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._color = None

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_color(self, color):
        self._color = color

    def get_color(self):
        return self._color


def worker(w_idx, w_cnt, w_points, w_cfg, q, e):

    w_point_idx = w_idx

    while True:

        if w_point_idx >= len(w_points):
            break

        if e.is_set():
            break

        w_point = w_points[w_point_idx]

        print('processing ' + repr(w_point.get_x()) + ':' + repr(w_point.get_y()) + ' by worker ' + repr(w_idx))

        init_pos = np.array([w_point.get_x(), w_point.get_y()])
        init_vel = np.array([0, 0])

        integ = it.RungeKutta4th(DiffEq(w_cfg), init_pos, init_vel)
        obs = Observer(w_cfg, None)
        integ.execute(w_cfg.m_fTimeStep, w_cfg.m_nMaxSteps, observer=obs)

        if not obs.get_closest_src() is None:
            clr = obs.get_closest_src().get_color()
        else:
            clr = 'b'

        result = Point(w_point.get_x(), w_point.get_y())
        result.set_color(clr)

        q.put(result)

        w_point_idx += w_cnt


def animate(i):
    while not point_queue.empty():
        point = point_queue.get()
        ax.scatter(point.get_x(), point.get_y(), c=point.get_color(), s=10)


if __name__ == '__main__':

    cfg = TriangleConfig()

    worker_count = 10

    # -- setup worker

    points = []

    for x in range(0, cfg.m_fSimWidth, 18):
        for y in range(0, cfg.m_fSimHeight, 18):
            points.append(Point(x, y))

    point_queue = Queue()
    terminate_event = Event()

    processes = []
    for worker_index in range(0, worker_count):
        process = Process(target=worker, args=(worker_index, worker_count, points, cfg, point_queue, terminate_event))
        process.start()
        processes.append(process)

    # -- setup plot

    fig, ax = plt.subplots()

    ax.set_title('Magnetpendel Path')

    ax.set_xlabel('x', fontsize=15)
    ax.set_xlim(0, cfg.m_fSimWidth)

    ax.set_ylabel('y', fontsize=15)
    ax.set_ylim(0, cfg.m_fSimHeight)

    ax.grid(False)
    fig.tight_layout()

    anim = animation.FuncAnimation(fig, animate, interval=500)

    plt.show()

    terminate_event.set()

    for process in processes:
        process.join()
