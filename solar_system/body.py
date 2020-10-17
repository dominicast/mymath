
class Body:

    def __init__(self, m, r, sp, sv):
        self._m = m
        self._r = r
        self._sp = sp
        self._sv = sv
        self._index = None

    def get_m(self):
        return self._m

    def get_r(self):
        return self._r

    def get_sp(self):
        return self._sp

    def get_sv(self):
        return self._sv

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index


class VisibleBody(Body):

    def __init__(self, m, r, sp, sv, color, size, pos_mapper=None):
        Body.__init__(self, m, r, sp, sv)
        self._color = color
        self._size = size
        self._pos_mapper = pos_mapper
        self._object = None

    def get_color(self):
        return self._color

    def get_size(self):
        return self._size

    def get_x(self, x):
        return x if self._pos_mapper is None else self._pos_mapper.map(x)

    def get_y(self, y):
        return y if self._pos_mapper is None else self._pos_mapper.map(y)

    def get_z(self, z):
        return z if self._pos_mapper is None else self._pos_mapper.map(z)

    def get_object(self):
        return self._object

    def set_object(self, object):
        self._object = object
