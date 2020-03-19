#! /usr/bin/python3
# -*- coding: utf-8 -*-


__author__ = 'Alan Loh'
__copyright__ = 'Copyright 2020, cmspy'
__credits__ = ['Alan Loh']
__maintainer__ = 'Alan'
__email__ = 'alan.loh@obspm.fr'
__status__ = 'Production'
__all__ = [
    'MSParset'
]


from os.path import (
    join,
    abspath,
    dirname,
    isdir,
    isfile,
    basename
)
import zipfile
import numpy as np
import logging
import astropy.units as u
from astropy.time import Time, TimeDelta

from cmspy.Astro import to_skycoord
from cmspy.AntennaTable import nenufar_antennas


log = logging.getLogger(__name__)


# ============================================================= #
# ------------------------- MSParset -------------------------- #
# ============================================================= #
class MSParset(object):
    """
    """

    def __init__(self, **kwargs):
        self.msname = 'noname.ms'
        self.savepath = ''
        self.antennatable = 'nenufar'
        self.ra = 0 * u.deg
        self.dec = 90 * u.deg
        self.f0 = 50 * u.MHz
        self.df = 0.1953125 * u.MHz
        self.nf = 16
        self.nbands = 16
        self.t0 = Time.now()
        self.dt = TimeDelta(1, format='sec')
        self.nt = 10
        
        self._fill_attr(kwargs)


    # --------------------------------------------------------- #
    # --------------------- Getter/Setter --------------------- #
    @property
    def msname(self):
        return self._msname
    @msname.setter
    def msname(self, m):
        if basename(m) != m:
            raise ValueError(
                'Just provide the MS name, path is `savepath`'
            )
        if not m.endswith('.ms'):
            raise ValueError(
                'msname should ends with .ms'
            )
        self._msname = m
        return


    @property
    def savepath(self):
        return self._savepath
    @savepath.setter
    def savepath(self, s):
        s = abspath(s)
        if not isdir(s):
            raise NotADirectoryError(
                '{} not found'.format(s)
            )
        self._savepath = s
        return
    

    @property
    def antennatable(self):
        return self._antennatable
    @antennatable.setter
    def antennatable(self, a):
        if a.lower() == 'nenufar':
            a = nenufar_antennas
        else:
            raise ValueError(
                'Unexpected antenna distribution'
            )
        self._antennatable = a
        return
    

    @property
    def nbands(self):
        return self._nbands
    @nbands.setter
    def nbands(self, n):
        if not isinstance(n, int):
            raise TypeError(
                'nbands should be integer'
            )
        self._nbands = n
        return


    @property
    def nf(self):
        return self._nf
    @nf.setter
    def nf(self, n):
        if not isinstance(n, int):
            raise TypeError(
                'nf should be integer'
            )
        self._nf = n
        return


    @property
    def nt(self):
        return self._nt
    @nt.setter
    def nt(self, n):
        if not isinstance(n, int):
            raise TypeError(
                'nt should be integer'
            )
        self._nt = n
        return


    @property
    def t0(self):
        return self._t0
    @t0.setter
    def t0(self, t):
        if not isinstance(t, Time):
            t = Time(t)
        self._t0 = t
        return


    @property
    def dt(self):
        return self._dt
    @dt.setter
    def dt(self, d):
        if not isinstance(d, TimeDelta):
            d = TimeDelta(d, format='sec')
        self._dt = d
        return


    @property
    def ra(self):
        return self._ra
    @ra.setter
    def ra(self, r):
        if not isinstance(r, u.Quantity):
            r = float(r)
            r *= u.deg
        self._ra = r.to(u.deg)
        return


    @property
    def dec(self):
        return self._dec
    @dec.setter
    def dec(self, d):
        if not isinstance(d, u.Quantity):
            d = float(d)
            d *= u.deg
        self._dec = d.to(u.deg)
        return


    @property
    def f0(self):
        return self._f0
    @f0.setter
    def f0(self, f):
        if not isinstance(f, list):
            f = [f]
        if not all([isinstance(fi, u.Quantity) for fi in f]):
            f = [float(fi) * u.MHz for fi in f]
        self._f0 = [fi.to(u.Hz) for fi in f]
        return


    @property
    def df(self):
        return self._df
    @df.setter
    def df(self, d):
        if not isinstance(d, u.Quantity):
            d =  float(d)
            d *= u.MHz
        self._df = d.to(u.Hz)
        return


    # --------------------------------------------------------- #
    # ------------------------ Methods ------------------------ #
    def check_conformity(self):
        """ Once all attributes are set, this verifies that
            everything is convenient for being a makems parset.
        """
        conform = True
        if self.nf % self.nbands != 0:
            log.warning(
                'nf must be divisible by nbands'
            )
            conform *= False
        try:
            phase_center = to_skycoord((self.ra, self.dec))
        except ValueError:
            log.warning(
                'ra and dec are not properly set'
            )
            conform *= False
        if self.antennatable.endswith('.zip'):
            with zipfile.ZipFile(self.antennatable) as zipf:
                zipf.extractall(self.savepath)
            self._anttable = join(
                self.savepath,
                basename(self.antennatable).replace('.zip', '')
            )
            log.info(
                'Antenna table {} created.'.format(
                    self._anttable
                )
            )
        else:
            log.warning(
                'antenna table is expected as a zip file'
            )
            conform *= False
        if (len(self.f0) != 1) and (len(self.f0) != self.nbands):
            log.warning(
                'f0 sould either have a length=1 or =nbands'
            ) 
            conform *= False
        return bool(conform)


    def write_parset(self):
        """
        """
        if not self.check_conformity():
            raise Exception(
                'Attributes are not properly filled.'
            )
        log.info(
            'Parameters conform for empty MS creation'
        )
        config = {
            'MSName': join(self.savepath, self.msname),
            'VDSPath': self.savepath,
            'AntennaTableName': self._anttable,
            'WriteImagerColumns': 'T',
            'WriteAutoCorr': 'T',
            'Declination': '{}rad'.format(
                self.dec.to(u.rad).value
            ),
            'RightAscension': '{}rad'.format(
                self.ra.to(u.rad).value
            ),
            'StartFreq': [fi.to(u.Hz).value for fi in self.f0],
            'StepFreq': self.df.to(u.Hz).value,
            'NFrequencies': self.nf,
            'NBands': self.nbands,
            'StartTime': self.t0.isot.replace('T', '/'),
            'StepTime': self.dt.to(u.s).value,
            'NTimes': self.nt
        }
        parsetfile = join(self.savepath, 'makems.cfg')
        parset = open(parsetfile, 'w')
        for key in config.keys():
            parset.write(
                '{} = {}\n'.format(key, config[key])
            )
        parset.close()
        log.info(
            'Parset {} written'.format(parsetfile)
        )
        return


    # --------------------------------------------------------- #
    # ----------------------- Internal ------------------------ #
    def _fill_attr(self, kwargs):
        """
        """
        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)
        return
# ============================================================= #

