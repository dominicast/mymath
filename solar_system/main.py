
from mayavi import mlab
from config_solar_system import Config
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

        pos = solver.process(frame_dt)

        # ---

        view = mlab.view()
        if view is not None:
            view_distance = view[2]

        scene.disable_render = True

        for body in bodies:
            index = body.get_index()
            x = body.get_x(pos[index, 0])
            y = body.get_y(pos[index, 1])
            z = body.get_z(pos[index, 2])
            body.get_object().set(x=x, y=y, z=z)
            if body.get_label() is not None and view is not None:
                body.get_label().position = [x+(body.get_size()/2), y+(body.get_size()/2), z+(body.get_size()/2)]
                body.get_label().scale = [view_distance/100, view_distance/100, view_distance/100]

        scene.disable_render = False

        yield


if __name__ == '__main__':

    config = Config()
    bodies = config.get_bodies()

    for body in bodies:
        sp = body.get_sp()[0]
        x = body.get_x(sp[0])
        y = body.get_y(sp[1])
        z = body.get_z(sp[2])
        distance = str(math.sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2)))
        print('{name}: distance={distance} size={size}'.format(name=body.get_name(), distance=distance, size=body.get_size()))

    G = config.get_G()
    speed = config.get_speed()
    dt = config.get_dt()

    solver = Solver(bodies, G, Logger())

    fig = mlab.figure(size=(1000,600), bgcolor=(0., 0., 0.))
    # fig.scene.anti_aliasing_frames = 0

    for body in bodies:
        sp = body.get_sp()[0]
        x = body.get_x(sp[0])
        y = body.get_y(sp[1])
        z = body.get_z(sp[2])
        color = body.get_color()
        size = body.get_size()
        pts = mlab.points3d(x, y, z, color=color, scale_factor=size)
        body.set_object(pts.mlab_source)
        if config.show_names():
            lbl = mlab.text3d(x, y, z, body.get_name(), color=color)
            body.set_label(lbl)

    mlab.view(
        azimuth=config.get_azimuth(),
        elevation=config.get_elevation(),
        distance=config.get_distance()
    )

    a = anim(bodies, solver, fig.scene, speed)

    mlab.show()
