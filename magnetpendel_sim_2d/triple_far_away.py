
from source import *

class TriangleConfig:

    m_fSimWidth = 1000
    m_fSimHeight = 1000

    m_fFriction = 0.0006
    m_fHeight = 10
    m_fTimeStep = 1.5
    m_nMinSteps = 1000
    m_nMaxSteps = 80000
    m_fAbortVel = 0.1

    sources = []

    def __init__(self):

        # pendulum force
        self.sources.append(Source(0, 0, 0.000001, 0, SourceType.LINEAR, False, False, ''))

        # magnets
        self.sources.append(Source(60, 90, 5, 5, SourceType.INV_SQR, True, True, 'r'))
        self.sources.append(Source(60, 210, 5, 5, SourceType.INV_SQR, True, True, 'g'))
        self.sources.append(Source(60, 330, 5, 5, SourceType.INV_SQR, True, True, 'b'))
