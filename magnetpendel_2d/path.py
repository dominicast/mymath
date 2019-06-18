
from path_plotter import *
from path_pendulum import PathPendulum
from config import *

import matplotlib.pyplot as plt
from matplotlib import animation


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
    speed = cfg.get_speed()

    return PathPendulum(magnets, mount_point, distance, friction, m, abort_velocity, min_steps, max_steps, dt, speed)


def animate(i, pendulum, plotter):
    data = pendulum.calculate_frame()
    plotter.plot_frame(data)


# by Dominic Ast D! dominic_ast@gmx.ch
if __name__ == '__main__':

    config = BigTriangleConfig().get_config(Action.SHOW)

    start_pos = config.get_start_pos()
    start_vel = config.get_start_vel()

    # -- setup plot

    fig, ax = plt.subplots()

    plotter = Plotter(ax)
    plotter.setup(config.get_width(), config.get_height())
    fig.tight_layout()
    plotter.plot_situation(config.get_magnets())

    # -- pendulum

    pendulum = create_pendulum(config)
    pendulum.init_deq(start_pos, start_vel)
    pendulum.start()

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
