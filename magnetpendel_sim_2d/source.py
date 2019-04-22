
from enum import Enum

class SourceType(Enum):
    LINEAR = 1
    INV = 2
    INV_SQR = 3

class Source:

    def __init__(self, rad, theta, mult, size, type, show, is_magnet, color):
        self._rad = rad
        self._theta = theta
        self._mult = mult
        self._size = size
        self._type = type
        self._show = show
        self._is_magnet = is_magnet
        self._color = color

    def set_pos(self, pos):
        self._pos = pos

    def get_pos(self):
        return self._pos

    def get_rad(self):
        return self._rad

    def get_theta(self):
        return self._theta

    def get_mult(self):
        return self._mult

    def get_size(self):
        return self._size

    def get_type(self):
        return self._type

    def get_show(self):
        return self._show

    def get_is_magnet(self):
        return self._is_magnet

    def get_color(self):
        return self._color
