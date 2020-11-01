
from mayavi import mlab


class Plotter:

    def __init__(self, bodies, projector):
        self._bodies = bodies
        self._projector = projector
        self._fig = None

    def initialize(self, config):

        self._fig = mlab.figure(size=(1000, 600), bgcolor=(0., 0., 0.))
        # self._fig.scene.anti_aliasing_frames = 0

        for body in self._bodies:
            pos_p = self._projector.get_pos(body)
            size_p = self._projector.get_size(body)
            color = body.get_color()
            pts = mlab.points3d(pos_p[0], pos_p[1], pos_p[1], color=color, scale_factor=size_p)
            body.plt_point = pts.mlab_source
            if config.show_names():
                body.plt_label = mlab.text3d(pos_p[0], pos_p[1], pos_p[2], body.get_name(), color=color)
            else:
                body.plt_label = None

        mlab.view(
            azimuth=config.get_azimuth(),
            elevation=config.get_elevation(),
            distance=config.get_distance()
        )

    def update(self):

        scene = self._fig.scene

        if scene is None:
            return

        view = mlab.view()
        if view is not None:
            view_distance = view[2]

        scene.disable_render = True

        for body in self._bodies:

            pos_p = self._projector.get_pos(body)
            body.plt_point.set(
                x=pos_p[0],
                y=pos_p[1],
                z=pos_p[2]
            )

            if body.plt_label is not None and view is not None:

                size_p = self._projector.get_size(body)

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
