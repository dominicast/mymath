
import integ as it

import math
import numpy as np


class DiffEq:

    def __init__(self, G, bodies):
        self._G = G
        self._bodies = bodies

    def f(self, pos, vel, t):

        G = self._G

        result = np.zeros((len(self._bodies), 3))

        for body_1 in self._bodies:

            m_b1 = body_1.get_m()
            p_b1 = pos[body_1.solver_idx]

            for body_2 in self._bodies:
                if body_2.solver_idx <= body_1.solver_idx:
                    continue

                m_b2 = body_2.get_m()
                p_b2 = pos[body_2.solver_idx]

                r = p_b2 - p_b1
                r_len = math.sqrt(r[0] ** 2 + r[1] ** 2 + r[2] ** 2)

                factor = G * ((m_b1 * m_b2) / (r_len ** 3))

                F_b1 = factor * r
                a_b1 = (F_b1 / m_b1)
                result[body_1.solver_idx] = result[body_1.solver_idx] + a_b1

                F_b2 = factor * -r
                a_b2 = (F_b2 / m_b2)
                result[body_2.solver_idx] = result[body_2.solver_idx] + a_b2

        return result


class Solver:

    def __init__(self, bodies, G, logger=None):

        self._bodies = bodies

        sp = np.zeros((len(bodies), 3))
        sv = np.zeros((len(bodies), 3))

        index = 0
        for body in bodies:
            body.solver_idx = index
            sp[body.solver_idx] = body.get_pos()
            sv[body.solver_idx] = body.get_vel()
            index += 1

        # self._deq = it.RungeKutta4th(DiffEq(u.get_m(), v.get_m()), sp, sv, 10)
        self._deq = it.SciPy(DiffEq(G, bodies), sp, sv, None, logger)

    def process(self, t_delta):
        pos, vel, _, _ = self._deq.process_td(t_delta)
        for body in self._bodies:
            body.set_pos(pos[body.solver_idx])
            body.set_vel(vel[body.solver_idx])
