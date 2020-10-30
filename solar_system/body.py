
class Body:

    def __init__(self, name, m, r, color, pos, vel):
        self._name = name
        self._m = m
        self._r = r
        self._pos = pos
        self._vel = vel
        self._color = color

    def get_name(self):
        return self._name

    def get_m(self):
        return self._m

    def get_r(self):
        return self._r

    def get_color(self):
        return self._color

    def get_pos(self):
        return self._pos

    def set_pos(self, pos):
        self._pos = pos

    def get_vel(self):
        return self._vel

    def set_vel(self, vel):
        self._vel = vel


class SimulationBody(Body):

    def __init__(self, name, m, r, color, pos, vel):
        Body.__init__(self, name, m, r, color, pos, vel)
        self._index = None
        self._object = None
        self._label = None
        self._projection = None

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index

    def get_object(self):
        return self._object

    def set_object(self, object):
        self._object = object

    def get_label(self):
        return self._label

    def set_label(self, label):
        self._label = label

    def get_projection(self):
        return self._projection

    def set_projection(self, projection):
        self._projection = projection
