import matplotlib.pyplot as plt
from matplotlib import animation
import integ as it
from config.triangle import *
from mp.eq import DiffEq
from mp.observer import Observer
import numpy as np
from threading import Lock
import threading


# Display path from init_pos with velocity init_vel
# to one of the magnets


cfg = TriangleConfig()

# -- setup plot

fig, ax = plt.subplots()

ax.set_title('Magnetpendel Path')

ax.set_xlabel('x', fontsize=15)
ax.set_xlim(0, cfg.m_fSimWidth)

ax.set_ylabel('y', fontsize=15)
ax.set_ylim(0, cfg.m_fSimHeight)

ax.grid(False)
fig.tight_layout()

# -- simulate equation

class Point:

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._color = None
        self._progressing = False
        self._printed = False

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_color(self, color):
        self._color = color

    def get_color(self):
        return self._color

    def set_progressing(self):
        self._progressing = True

    def get_progressing(self):
        return self._progressing

    def set_printed(self):
        self._printed = True

    def get_printed(self):
        return self._printed


def worker(tid):
    global points_proc_idx

    while True:

        my_point = None

        lock.acquire()
        if points_proc_idx < len(points):
            my_point = points[points_proc_idx]
            my_point.set_progressing()
            points_proc_idx += 1
        lock.release()

        if my_point is None:
            break

        print('processing ' + repr(my_point.get_x()) + ':' + repr(my_point.get_y()) + ' by thread ' + tid )

        init_pos = np.array([my_point.get_x(), my_point.get_y()])
        init_vel = np.array([0, 0])

        integ = it.RungeKutta4th(DiffEq(cfg), init_pos, init_vel)
        obs = Observer(cfg, None)
        integ.execute(cfg.m_fTimeStep, cfg.m_nMaxSteps, observer=obs)

        if not obs.get_closest_src() is None:
            clr = obs.get_closest_src().get_color()
        else:
            clr = 'b'

        my_point.set_color(clr)


points = []
points_proc_idx = 0
points_print_idx = 0

for x in range(0, cfg.m_fSimWidth, 18):
    for y in range(0, cfg.m_fSimHeight, 18):
        points.append(Point(x, y))

lock = Lock()

threads = []

for i in range(0, 5):
    t = threading.Thread(target=worker, args=('thread'+repr(i),))
    threads.append(t)
    t.start()

def animate(i):
    global points_print_idx

    while True:

        print("!!!!!")

        if points_print_idx >= len(points):
            return

        point = points[points_print_idx]

        if point.get_color() is None:
            break

        if point.get_printed():
            continue

        ax.scatter(point.get_x(), point.get_y(), c=point.get_color(), s=10)
        point.set_printed()

        points_print_idx += 1

anim = animation.FuncAnimation(fig, animate, interval=500)


plt.show()

# -- display plot


