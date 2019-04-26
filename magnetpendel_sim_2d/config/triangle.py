from mp.source import *
from config.config import ConfigBase


class TriangleConfig(ConfigBase):

    m_fSimWidth = 800
    m_fSimHeight = 800

    m_fFriction = 0.0005
    m_fHeight = 10
    m_fTimeStep = 1
    m_nProbeModulo = 20
    m_nMinSteps = 1000
    m_nMaxSteps = 500000
    m_fAbortVel = 0.04

    sources = []

    def __init__(self):

        # pendulum force
        self.sources.append(Source(0, 0, 0.000005, 1, SourceType.LINEAR, False, False, 'k'))

        # magnets
        self.sources.append(Source(170, 90, 10, 10, SourceType.INV_SQR, True, True, 'r'))
        self.sources.append(Source(170, 210, 10, 10, SourceType.INV_SQR, True, True, 'g'))
        self.sources.append(Source(170, 330, 10, 10, SourceType.INV_SQR, True, True, 'b'))

        self.calc_positions()
