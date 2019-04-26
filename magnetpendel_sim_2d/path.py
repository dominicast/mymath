import matplotlib.pyplot as plt
import integ as it
from config.triangle import *
from mp.eq import DiffEq
from mp.observer import Observer
import numpy as np


# Display path from init_pos with velocity init_vel
# to one of the magnets


class PathObserver(Observer):

    def _step_done(self, pos, n):
        if n % self._cfg.m_nProbeModulo == 0:
            ax.scatter(pos[0], pos[1], c='k', s=0.01)

    def _process_done(self):
        pass


cfg = TriangleConfig()

#init_pos = np.array([200,600])
init_pos = np.array([800,800])

init_vel = np.array([0,0])

# -- setup plot

fig, ax = plt.subplots()

ax.set_title('Magnetpendel Path')

ax.set_xlabel('x', fontsize=15)
ax.set_xlim(0, cfg.m_fSimWidth)

ax.set_ylabel('y', fontsize=15)
ax.set_ylim(0, cfg.m_fSimHeight)

ax.grid(True)
fig.tight_layout()

# -- plot initial situation

for src in cfg.sources:
    if src.get_show():
        ax.scatter( src.get_pos()[0], src.get_pos()[1], c=src.get_color(), s=src.get_size()*50)

ax.scatter(init_pos[0], init_pos[1], s=2)
ax.arrow(init_pos[0], init_pos[1], init_vel[0], init_vel[1], fc='r', ec='r', width=0.01, head_width=1, head_length=1)

# -- simulate equation

integ = it.RungeKutta4th( DiffEq(cfg), init_pos, init_vel )

obs = PathObserver(cfg)

integ.execute( cfg.m_fTimeStep, cfg.m_nMaxSteps, observer=obs )

# -- display plot

if not obs.get_closest_src() is None:
    print( obs.get_closest_src().get_color() + ' : ' + repr( obs.get_n() ) + ' : ' + repr( obs.get_len() ) )
else:
    print( 'did not end' )

plt.show()
