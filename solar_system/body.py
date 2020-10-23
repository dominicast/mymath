
class Body:

    def __init__(self, name, m, r, color):
        self._name = name
        self._m = m
        self._r = r
        self._color = color

    def get_name(self):
        return self._name

    def get_m(self):
        return self._m

    def get_r(self):
        return self._r

    def get_color(self):
        return self._color


class SimulationBody(Body):

    def __init__(self, name, m, r, color, sp, sv, size, displacer=None):
        Body.__init__(self, name, m, r, color)
        self._sp = sp
        self._sv = sv
        self._size = size
        self._displacer = displacer
        self._index = None
        self._object = None

    def get_sp(self):
        return self._sp

    def get_sv(self):
        return self._sv

    def get_size(self):
        return self._size

    def get_x(self, x):
        return x if self._displacer is None else self._displacer.map(x)

    def get_y(self, y):
        return y if self._displacer is None else self._displacer.map(y)

    def get_z(self, z):
        return z if self._displacer is None else self._displacer.map(z)

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index

    def get_object(self):
        return self._object

    def set_object(self, object):
        self._object = object
