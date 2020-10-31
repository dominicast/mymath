
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
