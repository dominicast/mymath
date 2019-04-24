from config.triangle import *
import numpy as np
import math


class DiffEq:

    def __init__(self, cfg):
        self._cfg = cfg

    def f(self, pos, vel, t):

        result = np.array([0,0])

        for src in self._cfg.sources:

            r = pos - src.get_pos()

            dist = math.sqrt( math.pow( r[0], 2 ) + math.pow( r[1], 2 ) + math.pow( self._cfg.m_fHeight, 2 ) )

            if src.get_type() == SourceType.LINEAR:
                force = src.get_mult() * r
            elif src.get_type() == SourceType.INV:
                force = (src.get_mult() / math.pow(dist, 2)) * r
            elif src.get_type() == SourceType.INV_SQR:
                force = (src.get_mult() / math.pow(dist, 3)) * r
            else:
                raise Exception( "Invalid source type " + repr( src.get_type() ) )

            result = result - force

        result = result - vel * self._cfg.m_fFriction

        return result
