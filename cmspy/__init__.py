#! /usr/bin/python3
# -*- coding: utf-8 -*-


__author__ = 'Alan Loh'
__copyright__ = 'Copyright 2020, cmspy'
__credits__ = ['Alan Loh']
__license__ = 'MIT'
__version__ = '0.0.1'
__maintainer__ = 'Alan Loh'
__email__ = 'alan.loh@obspm.fr'


import logging
import sys


logging.basicConfig(
    #filename='cmspy_MeasurementSet.log',
    #filemode='w',
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s -- %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

