
from pattern_plotter import *
from pendulum import Pendulum
from config import *

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

from multiprocessing import Process, Queue, Event


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


def create_pendulum(cfg):

    magnets = cfg.get_magnets()
    mount_point = cfg.get_mount_point()
    distance = cfg.get_distance()
    friction = cfg.get_friction()
    m = cfg.get_m()

    abort_velocity = cfg.get_abort_velocity()
    min_steps = cfg.get_min_steps()
    max_steps = cfg.get_max_steps()

    dt = cfg.get_dt()

    return Pendulum(magnets, mount_point, distance, friction, m, abort_velocity, min_steps, max_steps, dt)


def worker(w_idx, w_cnt, w_points, w_cfg, q, e):

    w_point_idx = w_idx

    chunk_size = w_cfg.get_dt_chunk_size()

    while True:

        if w_point_idx >= len(w_points):
            break

        if e.is_set():
            break

        w_point = w_points[w_point_idx]

        # -- pendulum

        start_pos = np.array([w_point.get_x(), w_point.get_y()])
        start_vel = np.array([0, 0])

        pendulum = create_pendulum(w_cfg)
        pendulum.init_deq(start_pos, start_vel)

        while True:
            data = pendulum.calculate_frame(chunk_size)
            if data.get_done():
                break

        # --

        result = Point(w_point.get_x(), w_point.get_y())
        result.set_color(data.get_source().get_color())
        result.set_found(data.get_found())

        q.put(result)

        w_point_idx += w_cnt


def animate(i, plotter):
    while not point_queue.empty():
        point = point_queue.get()
        plotter.plot_point(point)


# by Dominic Ast D! dominic_ast@gmx.ch
if __name__ == '__main__':

    config = TriangleConfig().get_config(Action.SHOW)

    # -- setup plot

    fig, ax = plt.subplots()

    plotter = Plotter(ax, config.get_point_size())
    plotter.setup(config.get_width(), config.get_height())
    fig.tight_layout()

    # -- setup points

    points = []

    point_delta = config.get_point_delta()

    x_to = config.get_width()
    x_from = -(config.get_width() - (point_delta/2))

    y_to = config.get_height()
    y_from = -(config.get_height() - (point_delta/2))

    for x in np.arange(x_from, x_to, point_delta):
        for y in np.arange(y_from, y_to, point_delta):
            points.append(Point(x, y))

    # -- setup workers

    point_queue = Queue()
    terminate_event = Event()

    worker_count = config.get_worker_count()

    processes = []
    for worker_index in range(0, worker_count):
        process = Process(target=worker, args=(worker_index, worker_count, points, config, point_queue, terminate_event))
        process.start()
        processes.append(process)

    # -- run

    anim = animation.FuncAnimation(fig, animate, interval=500, fargs=(plotter,))

    plt.show()

    terminate_event.set()

    for process in processes:
        process.join()
