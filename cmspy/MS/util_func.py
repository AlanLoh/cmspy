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


from cmspy.Astro import radec2lmn

import numpy as np
import numba


# ============================================================= #
# ------------------------ compute_ft ------------------------- #
# ============================================================= #
@numba.jit(nopython=True, parallel=True,fastmath=True)
def compute_ft(ul, vm, wn):
    """
    """
    return np.exp(-2.j*np.pi*(ul + vm + wn))
# ============================================================= #


# ============================================================= #
# -------------------------- add_src -------------------------- #
# ============================================================= #
def add_src(uvw, src_coord, flux, phase_center):
    """
        :param uvw:
            UVW coordinates (baselines x time x spw, chans, 3),
            they should be converted in lambdas.
        :type uvw:
            `np.ndarray`

        :returns: vis
        :rtype: `np.ndarray`
    """
    l, m, n = radec2lmn(
        skycoord=src_coord,
        phase_center=phase_center
    )
    ul = uvw[..., 0] * l
    vm = uvw[..., 1] * m
    wn = uvw[..., 2] * (n - 1)
    return flux * compute_ft(ul, vm, wn)
# ============================================================= #

