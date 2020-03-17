#! /usr/bin/python3
# -*- coding: utf-8 -*-


__author__ = 'Alan Loh'
__copyright__ = 'Copyright 2020, cmspy'
__credits__ = ['Alan Loh']
__maintainer__ = 'Alan'
__email__ = 'alan.loh@obspm.fr'
__status__ = 'Production'
__all__ = [
    'to_skycoord',
    'radec2lmn'
]


import numpy as np
from astropy.coordinates import (
    SkyCoord
)
import astropy.units as u


# ============================================================= #
# ------------------------ to_skycoord ------------------------ #
# ============================================================= #
def to_skycoord(coord):
    """
    """
    ra, dec = coord
    return SkyCoord(
        ra,
        dec,
        unit='deg',
        frame='icrs'
    )
# ============================================================= #


# ============================================================= #
# ------------------------- radec2lmn ------------------------- #
# ============================================================= #
def radec2lmn(skycoord, phase_center):
    """ Convert equatorial coordinates of a source to image
        domain coordinates, namely (l, m, n). Particularly useful
        while predicting visibilities. 

        :param skycoord:
            Equatorial coordinates of the source to be converted
            into image domain (l, m, n) coordinates.
        :type skycoord:
            `tuple` or :class:`astropy.coordinates.SkyCoord`
        :param phase_center:
            Phase center of the observation.

        :type phase_center:
            `tuple` or :class:`astropy.coordinates.SkyCoord`

        :returns: (l, m, n) coordinates
        :rtype: `tuple`

        :Example:

        >>> from cmspy.Astro import radec2lmn
        >>> radec2lmn(
                skycoord=(299.8681, 40.7339),
                phase_center=(0, 90)
            )

    """
    if not isinstance(skycoord, SkyCoord):
        skycoord = to_skycoord(skycoord)
    if not isinstance(phase_center, SkyCoord):
        phase_center = to_skycoord(phase_center)

    r = skycoord.ra.rad
    d = skycoord.dec.rad
    r0 = phase_center.ra.rad
    d0 = phase_center.dec.rad
    dr = r - r0

    l = np.cos(d)*np.sin(dr)
    m = np.sin(d)*np.cos(d0) -\
        np.cos(d)*np.sin(d0)*np.cos(dr)
    n = np.sqrt(1 - l**2. - m**2.)

    return l, m, n
# ============================================================= #

