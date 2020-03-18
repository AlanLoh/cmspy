#! /usr/bin/python3
# -*- coding: utf-8 -*-


__author__ = 'Alan Loh'
__copyright__ = 'Copyright 2020, cmspy'
__credits__ = ['Alan Loh']
__maintainer__ = 'Alan'
__email__ = 'alan.loh@obspm.fr'
__status__ = 'Production'
__all__ = [
    'nenufar_antennas'
]


from os.path import (
    join,
    dirname
)


nenufar_antennas = join(
    dirname(__file__),
    'NENUFAR_ANTENNA.zip',
)