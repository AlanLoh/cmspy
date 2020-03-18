#! /usr/bin/python3
# -*- coding: utf-8 -*-


__author__ = 'Alan Loh'
__copyright__ = 'Copyright 2020, cmspy'
__credits__ = ['Alan Loh']
__maintainer__ = 'Alan'
__email__ = 'alan.loh@obspm.fr'
__status__ = 'Production'
__all__ = [
    'add_src'
]


from casacore.tables import table


# ============================================================= #
# -------------------------- add_src -------------------------- #
# ============================================================= #
def add_src(msname, ra, dec, flux):
    """
    """
    # Get visibilities
    # Get UVW coordinates
    # Get phase center
    # Convert src coordinates to (l, m, n)
    l, m, n = to_lmn(ra, dec, ra_0, dec_0)
    # Compute the phase
    ul = u*l[:, na, na, na]
    vm = v*m[:, na, na, na]
    nw = (n[:, na, na, na] - 1)*w
    phase = np.exp(-2.j*np.pi*(ul + vm + nw))
    # Add that to existing visibilities
    vis_model += flux * phase[..., na]
    return
# ============================================================= #

