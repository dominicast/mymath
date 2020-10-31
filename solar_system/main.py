
from mayavi import mlab
from config_solar_system import Config
# from config_earth import Config
# from config_2_body import Config
from solver import Solver
from plotter import Plotter
import time
import math


@mlab.animate(ui=False, delay=100)
def anim(solver, plotter, speed):

    ts_save = time.time()
    day_save = 0

    yield

    t = 0

    while True:

        ts = time.time()
        frame_dt = (ts - ts_save) * speed
        ts_save = ts
        t = t + frame_dt

        day = int(t/60/60/24)
        if day != day_save:
            day_save = day
            year = int(day / 365)
            day -= 365 * year
            print("Year {year}, Day {day}".format(year=year, day=day))

        solver.process(frame_dt)

        plotter.update()

        yield


if __name__ == '__main__':

    config = Config()
    projector = config.create_projector()
    bodies = config.get_bodies()
    solver = Solver(bodies, config.get_G())
    plotter = Plotter(bodies, projector)

    for body in bodies:
        pos_p = projector.get_pos(body)
        size_p = projector.get_size(body)
        distance = str(math.sqrt(pow(pos_p[0], 2) + pow(pos_p[1], 2) + pow(pos_p[2], 2)))
        print('{name}: distance={distance} size={size}'.format(
            name=body.get_name(),
            distance=distance,
            size=size_p
        ))

    plotter.initialize(config)

    a = anim(solver, plotter, config.get_speed())

    mlab.show()
