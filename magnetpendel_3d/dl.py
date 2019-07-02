
from config import *


class DlConfig(BaseConfig):

    def get_config(self, action):
        config = super()._get_config()

        config._name = 'leiner'

        config._width = 0.3
        config._height = 0.3
        config._depth = 0.3

        config._mount_point = MountPoint(np.array([0, 0, 0.3]), 0.01, 0.0025, 'k')

        config._start_pos = self._room_position_xy(config._mount_point.get_pos(), 0.25, 0.1, 0.1)
        config._start_vel = np.array([0, 0, 0])
        config._m = 0.5

        magnets = [
            Magnet(self._floor_position(0.1, 0), 0.02, 0.025, 'r'),
            Magnet(self._floor_position(0.1, 120), 0.02, 0.025, 'g'),
            Magnet(self._floor_position(0.1, 240), 0.02, 0.025, 'b')
        ]
        config._magnets = magnets

        config._friction = 0.001

        config._action = action

        if config.get_action() == Action.HTML:
            config._frames = 64

        config._dt = 0.001

        config._interval = 100
        config._speed = 1

        # config._math_utils = MathUtilsDl()

        return config


class MathUtilsDl:

    @staticmethod
    def _xy_to_rad(ol, al):

        if al == 0:
            if ol >= 0:
                return math.pi/2
            else:
                return 3*math.pi/2

        angle = math.atan(abs(ol/al))

        if al >= 0:
            if ol >= 0:
                return angle
            else:
                return (2*math.pi)-angle
        else:
            if ol >= 0:
                return math.pi - angle
            else:
                return math.pi + angle

    def unit_vec_ps(self, vec):

        ol = math.sqrt(vec[0]**2 + vec[1]**2)
        al = -vec[2]
        alpha = self._xy_to_rad(ol, al)

        ol = vec[1]
        al = vec[0]
        beta = self._xy_to_rad(ol, al)

        x = math.cos(alpha) * math.cos(beta)
        y = math.cos(alpha) * math.sin(beta)
        z = -math.sin(alpha)

        return np.array([x, y, z])

    def unit_vec_v(self, vec):

        ol = vec[2]
        al = math.sqrt(vec[0]**2 + vec[1]**2)
        phi = self._xy_to_rad(ol, al)

        ol = vec[1]
        al = vec[0]
        epsilon = self._xy_to_rad(ol, al)

        x = math.cos(phi) * math.cos(epsilon)
        y = math.cos(phi) * math.sin(epsilon)
        z = math.sin(phi)

        return np.array([x, y, z])

    def unit_vec_r(self, vec):

        vec = -vec

        theta, phi = self.spherical_coords_mp(vec)

        x = (-1) * math.sin(theta) * math.cos(phi)
        y = (-1) * math.sin(theta) * math.sin(phi)
        z = math.cos(theta)

        return np.array([x, y, z])

    def spherical_coords_mp(self, vec):
        ol = math.sqrt(vec[0]**2 + vec[1]**2)
        al = -vec[2]
        gamma = self._xy_to_rad(ol, al)

        ol = vec[1]
        al = vec[0]
        delta = self._xy_to_rad(ol, al)

        return gamma, delta
