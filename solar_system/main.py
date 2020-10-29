
from mayavi import mlab
from config_solar_system import Config
# from config_earth import Config
# from config_2_body import Config
from solver import Solver
import time
import math


class Logger:

    def log(self, tag, *values, level):
        pass

    def inc_level(self):
        pass

    def dec_level(self):
        pass


@mlab.animate(ui=False, delay=100)
def anim(bodies, solver, scene, speed):

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

        # ---

        pos, vel = solver.process(frame_dt)

        for body in bodies:
            body.set_pos(pos[body.get_index()])
            body.set_vel(vel[body.get_index()])

        # ---

        view = mlab.view()
        if view is not None:
            view_distance = view[2]

        scene.disable_render = True

        for body in bodies:
            pos_prime = body.get_pos_prime(bodies)
            body.get_object().set(
                x=pos_prime[0],
                y=pos_prime[1],
                z=pos_prime[2]
            )
            if body.get_label() is not None and view is not None:
                body.get_label().position = [
                    pos_prime[0]+(body.get_size()/2),
                    pos_prime[1]+(body.get_size()/2),
                    pos_prime[2]+(body.get_size()/2)
                ]
                body.get_label().scale = [
                    view_distance/100,
                    view_distance/100,
                    view_distance/100
                ]

        scene.disable_render = False

        yield


if __name__ == '__main__':

    config = Config()
    bodies = config.get_bodies()

    index = 0
    for body in bodies:
        body.set_index(index)
        index = index + 1

    for body in bodies:
        pos_prime = body.get_pos_prime(bodies)[0]
        distance = str(math.sqrt(pow(pos_prime[0], 2) + pow(pos_prime[1], 2) + pow(pos_prime[2], 2)))
        print('{name}: distance={distance} size={size}'.format(name=body.get_name(), distance=distance, size=body.get_size()))

    G = config.get_G()
    speed = config.get_speed()
    dt = config.get_dt()

    solver = Solver(bodies, G, Logger())

    fig = mlab.figure(size=(1000,600), bgcolor=(0., 0., 0.))
    # fig.scene.anti_aliasing_frames = 0

    for body in bodies:
        pos_prime = body.get_pos_prime(bodies)[0]
        color = body.get_color()
        size = body.get_size()
        pts = mlab.points3d(pos_prime[0], pos_prime[1], pos_prime[1], color=color, scale_factor=size)
        body.set_object(pts.mlab_source)
        if config.show_names():
            lbl = mlab.text3d(pos_prime[0], pos_prime[1], pos_prime[2], body.get_name(), color=color)
            body.set_label(lbl)

    mlab.view(
        azimuth=config.get_azimuth(),
        elevation=config.get_elevation(),
        distance=config.get_distance()
    )

    a = anim(bodies, solver, fig.scene, speed)

    mlab.show()
