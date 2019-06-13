
#from utils import *
from plotter import *
from pendulum import Pendulum
from config import *

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np


def animate(i, pendulum, plotter):
    data = pendulum.calculate_frame()
    plotter.plot_frame(data)


# by Dominic Ast D! dominic_ast@gmx.ch
if __name__ == '__main__':

    config = TriangleConfig().get_config(Action.SHOW)

    time_factor = config.get_time_factor()

    # -- situation

    # -- setup plot

    fig, ax = plt.subplots()

    plotter = Plotter(ax)
    plotter.setup(config.get_width(), config.get_height())
    fig.tight_layout()
    plotter.plot_situation(config.get_magnets())

    # -- integration

    integ_dt = config.get_integ_dt()
    integ_count = config.get_integ_count()
    integ_freq = config.get_integ_freq()

    if integ_dt * integ_count * 1000 != integ_freq:
        raise Exception('Invalid time configuration')

    integ_count = round(integ_count * time_factor)

    # -- pendulum

    magnets = config.get_magnets()
    mount_point = config.get_mount_point()
    distance = config.get_distance()
    friction = config.get_friction()
    m = config.get_m()

    pendulum = Pendulum(magnets, mount_point, distance, friction, m, integ_dt, integ_count)
    pendulum.init_deq(np.array([200, 600]), np.array([0, 0]))

    # -- run

    anim = animation.FuncAnimation(fig, animate, interval=integ_freq, fargs=(pendulum,plotter,), blit=False, frames=config.get_frames())

    if config.get_action() == Action.SHOW:
        plt.show()

    #elif config.get_action() == Action.HTML:

    #    print(animation.writers.list())

    #    Writer = animation.writers['html']
    #    writer = Writer(fps=15, metadata=dict(artist='Dominic Ast D!'), bitrate=1800)

    #    anim.save(config.get_name()+'.html', writer=writer)


    #else:
    #    raise Exception('Unknown action')
