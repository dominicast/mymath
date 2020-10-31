
from mayavi import mlab


class Plotter:

    def __init__(self):
        self._fig = None

    def initialize(self, bodies, projector, config):

        self._fig = mlab.figure(size=(1000, 600), bgcolor=(0., 0., 0.))
        # self._fig.scene.anti_aliasing_frames = 0

        for body in bodies:
            pos_p = projector.project(body, bodies)
            size_p = projector.scale(body, bodies)
            color = body.get_color()
            pts = mlab.points3d(pos_p[0], pos_p[1], pos_p[1], color=color, scale_factor=size_p)
            body.plt_point = pts.mlab_source
            if config.show_names():
                body.plt_label = mlab.text3d(pos_p[0], pos_p[1], pos_p[2], body.get_name(), color=color)

        mlab.view(
            azimuth=config.get_azimuth(),
            elevation=config.get_elevation(),
            distance=config.get_distance()
        )

    def update(self, bodies, projector):

        scene = self._fig.scene

        view = mlab.view()
        if view is not None:
            view_distance = view[2]

        scene.disable_render = True

        for body in bodies:

            pos_p = projector.project(body, bodies)
            body.plt_point.set(
                x=pos_p[0],
                y=pos_p[1],
                z=pos_p[2]
            )

            if body.plt_label is not None and view is not None:

                size_p = projector.scale(body, bodies)

                body.plt_label.position = [
                    pos_p[0]+(size_p/2),
                    pos_p[1]+(size_p/2),
                    pos_p[2]+(size_p/2)
                ]

                body.plt_label.scale = [
                    view_distance/100,
                    view_distance/100,
                    view_distance/100
                ]

        scene.disable_render = False
