import matplotlib.pyplot as plt
from matplotlib import animation
import integ as it
from config.triangle import *
from mp.eq import DiffEq
from mp.observer import Observer
import numpy as np
from multiprocessing import Process, Queue, Event


# Display the arising mapping pattern of all points
# on the canvas to the magnets


class Point:

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._color = None
        self._found = None

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_color(self, color):
        self._color = color

    def get_color(self):
        return self._color

    def get_found(self):
        return self._found

    def set_found(self, found):
        self._found = found


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
        integ.execute(w_cfg.m_fTimeStep, None, observer=obs)

        result = Point(w_point.get_x(), w_point.get_y())
        result.set_color(obs.get_closest_src().get_color())
        result.set_found(obs.get_found())

        q.put(result)

        w_point_idx += w_cnt


def animate(i):
    while not point_queue.empty():
        point = point_queue.get()
        if point.get_found():
            alpha = 1
        else:
            alpha = 0.5
        ax.scatter(point.get_x(), point.get_y(), c=point.get_color(), s=point_size, alpha=alpha)


if __name__ == '__main__':

    cfg = TriangleConfig()

    #worker_count = 10
    #point_size = 5
    #point_delta = 5

    worker_count = 1
    point_size = 15
    point_delta = 40

    # -- setup worker

    points = []

    for x in range(point_size, cfg.m_fSimWidth-(point_size-1), point_delta):
        for y in range(point_size, cfg.m_fSimHeight-(point_size-1), point_delta):
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

    ax.set_title('Magnetpendel Pattern')

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
