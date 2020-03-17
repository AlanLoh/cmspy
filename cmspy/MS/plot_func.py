#! /usr/bin/python3
# -*- coding: utf-8 -*-


__author__ = 'Alan Loh'
__copyright__ = 'Copyright 2020, cmspy'
__credits__ = ['Alan Loh']
__maintainer__ = 'Alan'
__email__ = 'alan.loh@obspm.fr'
__status__ = 'Production'
__all__ = [
    'plot_uv'
]


from casacore.tables import table

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


# ============================================================= #
# -------------------------- plot_uv -------------------------- #
# ============================================================= #
def plot_uv(msname, query=''):
    """
    """
    ms = table(
        tablename=msname,
        tabledesc=False,
        nrow=0,
        readonly=True,
        lockoptions='default',
        ack=True
    )
    if query != '':
        ms = ms.query(query)

    uvw = ms.getcol('UVW')

    ms.close()
    del ms

    fig, ax = plt.subplots(figsize=(10, 10))

    hbins = ax.hexbin(
        x=uvw[:, 0],
        y=uvw[:, 1],
        C=None,
        cmap='YlGnBu',
        mincnt=1,
        bins='log',
        gridsize=200,
        vmin=0.1,
        xscale='linear',
        yscale='linear',
        edgecolors='face',
        linewidths=0,
        vmax=None)

    ax.set_aspect('equal')
    ax.margins(0)
    
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size=0.15, pad=0.2)
    cb = fig.colorbar(hbins, cax=cax)
    
    cb.set_label('Histogram')
    ax.set_xlabel('u (m)')
    ax.set_ylabel('v (m)')

    lim = 1.1*np.max(
            (np.abs(ax.get_xlim()).max(),
            np.abs(ax.get_ylim()).max())
        )
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    plt.show()
    plt.close('all')
    return
# ============================================================= #


