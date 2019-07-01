
from utils import *
from plotter import *
from force import Pendulum
from config import *

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import juggle_axes
from matplotlib import animation
import numpy as np


def animate(i, pendulum, plotter):
    data = pendulum.calculate_frame()
    plotter.plot_frame(data)


# by Dominic Ast D! dominic_ast@gmx.ch
if __name__ == '__main__':

    config = DominickLeiner().get_config(Action.SHOW)
    math_utils = MathUtils()
    #math_utils = MathUtilsDl()

    #config = DominickLeiner().get_config(Action.SHOW)
    #math_utils = MathUtilsSc()

    # -- situation

    # mount point
    mp = config.get_mount_point().get_pos()

    # -- setup plot

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    plotter = Plotter(ax, mp)
    plotter.setup(config.get_width(), config.get_height(), config.get_depth())
    plotter.plot_situation(config.get_mount_point(), config.get_magnets())

    # -- pendulum

    mount_point = config.get_mount_point()
    start_pos = config.get_start_pos()
    start_vel = config.get_start_vel()

    magnets = config.get_magnets()
    friction = config.get_friction()
    m = config.get_m()
    g = config.get_g()

    dt = config.get_dt()
    speed = config.get_speed()

    pendulum = Pendulum(magnets, mount_point, friction, m, g, dt, speed, math_utils)
    pendulum.init_deq(start_pos, start_vel)

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
