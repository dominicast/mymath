
from config import *


class TriangleConfig(BaseConfig):

    def get_config(self, action):
        config = super()._get_config()

        config._name = 'triangle'

        config._width = 1
        config._height = 1
        config._depth = 1

        config._mount_point = MountPoint(np.array([0, 0, 1]), 0.01, 0.0025, 'k')

        config._start_pos = self._room_position_tp(config._mount_point.get_pos(), 0.9, 0.5, 0.2)
        #config._start_pos = self._room_position_tp(config._mount_point.get_pos(), 0.9, math.radians(40), math.radians(40))
        config._start_vel = np.array([0, 0, 0])

        magnets = [
            Magnet(self._floor_position(0.425, 90), 1, 0.04, 'r'),
            Magnet(self._floor_position(0.425, 210), 1, 0.04, 'g'),
            Magnet(self._floor_position(0.425, 330), 1, 0.04, 'b')
        ]
        config._magnets = magnets

        config._friction = 0.1

        config._action = action

        if config.get_action() == Action.HTML:
            config._frames = 256

        return config
