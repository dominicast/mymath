import sys
import os

# Add the additional source directory to sys.path
additional_src = os.path.join(os.path.dirname(__file__), '../common')
if additional_src not in sys.path:
    sys.path.append(additional_src)

from plotter import *
from pendulum import Pendulum
from dl import *
from triangle import *

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import juggle_axes
from matplotlib import animation


def animate(i, pendulum, plotter):
    data = pendulum.calculate_frame()
    plotter.plot_frame(data)

if __name__ == '__main__':

    # config = DlConfig().get_config(Action.SHOW)
    config = TriangleConfig().get_config(Action.SHOW)

    math_utils = config.get_math_utils()

    # -- setup plot

    fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # ax = fig.gca()
    ax = fig.add_subplot(111, projection='3d')

    plotter = Plotter(ax, config.get_mount_point().get_pos())
    plotter.setup(config.get_width(), config.get_height(), config.get_depth())
    plotter.plot_situation(config.get_mount_point(), config.get_magnets())

    # -- pendulum

    mount_point = config.get_mount_point()
    start_pos = config.get_start_pos()
    start_vel = config.get_start_vel()

    magnets = config.get_magnets()
    friction = config.get_friction()
    disturbance = config.get_disturbance()
    m = config.get_m()
    g = config.get_g()

    dt = config.get_dt()
    speed = config.get_speed()

    pendulum = Pendulum(magnets, mount_point, friction, disturbance, m, g, speed, math_utils)
    pendulum.init_deq(start_pos, start_vel, dt)

    # -- run

    anim = animation.FuncAnimation(fig, animate, interval=config.get_interval(), fargs=(pendulum,plotter,), blit=False, frames=config.get_frames())

    if config.get_action() == Action.SHOW:
        plt.show()

    elif config.get_action() == Action.HTML:

        print(animation.writers.list())

        Writer = animation.writers['html']
        writer = Writer(fps=15, metadata=dict(artist='Dominic Ast D!'), bitrate=1800)

        anim.save(config.get_name()+'.html', writer=writer)

    else:
        raise Exception('Unknown action')
