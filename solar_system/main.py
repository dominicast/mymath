
from mayavi import mlab
from config_solar_system import Config
# from config_earth import Config
# from config_2_body import Config
from solver import Solver
from plotter import Plotter
import time
import math


@mlab.animate(ui=False, delay=100)
def anim(bodies, solver, projector, plotter, speed):

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

        solver.process(bodies, frame_dt)

        plotter.update(bodies, projector)

        yield


if __name__ == '__main__':

    config = Config()

    bodies = config.get_bodies()
    projector = config.get_projector()
    G = config.get_G()
    speed = config.get_speed()

    solver = Solver(bodies, G)

    plotter = Plotter()

    for body in bodies:
        pos_p = projector.project(body, bodies)
        size_p = projector.scale(body, bodies)
        distance = str(math.sqrt(pow(pos_p[0], 2) + pow(pos_p[1], 2) + pow(pos_p[2], 2)))
        print('{name}: distance={distance} size={size}'.format(
            name=body.get_name(),
            distance=distance,
            size=size_p
        ))

    plotter.initialize(bodies, projector, config)

    a = anim(bodies, solver, projector, plotter, speed)

    mlab.show()
