import math
import numpy as np

class ConfigBase:

    def calc_positions(self):

        for src in self.sources:
            x = self.m_fSimWidth / 2 + src.get_rad() * math.cos(src.get_theta() * (math.pi / 180))
            y = self.m_fSimHeight / 2 + src.get_rad() * math.sin(src.get_theta() * (math.pi / 180))
            pos = np.array([x, y])
            src.set_pos(pos)
