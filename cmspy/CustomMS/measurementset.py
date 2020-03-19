#! /usr/bin/python3
# -*- coding: utf-8 -*-


__author__ = 'Alan Loh'
__copyright__ = 'Copyright 2020, cmspy'
__credits__ = ['Alan Loh']
__maintainer__ = 'Alan'
__email__ = 'alan.loh@obspm.fr'
__status__ = 'Production'
__all__ = [
    'MeasurementSet',
]


from cmspy.CustomMS import MSParset
from cmspy.MS import add_src
from cmspy.Astro import to_skycoord

from casacore.tables import table
import os
from os.path import join
import numpy as np
from astropy import constants as const
import logging


log = logging.getLogger(__name__)


# ============================================================= #
# ---------------------- MeasurementSet ----------------------- #
# ============================================================= #
class MeasurementSet(MSParset):
    """
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs
        )


    # --------------------------------------------------------- #
    # --------------------- Getter/Setter --------------------- #
    @property
    def msfile(self):
        return join(
            self.savepath,
            self.msname
        )


    @property
    def phase_center(self):
        ms = table(
            tablename=join(self.msfile, 'POINTING'),
            ack=False,
            readonly=True
        )
        center = to_skycoord(
            np.degrees(ms.getcol('TARGET')[0, 0])
        )
        ms.close()
        del ms
        return center
    
    

    # --------------------------------------------------------- #
    # ------------------------ Methods ------------------------ #
    def init_empty(self):
        """ Run `makems` to produce an empty MS thanks to the
            config file defined by current attributes of MSParset
        """
        self.write_parset()
        log.info(
            'Running makems to create empty MS {}...'.format(
                self.msfile
            )
        )
        result = os.system(
            'makems {}'.format(
                join(self.savepath, 'makems.cfg')
            )
        )
        if result == 32512:
            log.warning(
                'makems cannot be called.'
            )
            raise Exception(
                'Cannot run makems commmand line.'
            )
        log.info(
            'Empty MS {} created'.format(
                self.msfile
            )
        )
        return


    def add_desc_tables(self):
        """ Empty created MS is missing some required tables for
            further analysis with radio imager softwares.
        """
        # OBSERVATION table
        ms = table(
            tablename=join(self.msfile, 'OBSERVATION'),
            ack=False,
            readonly=False
        )
        observer = ms.getcol('OBSERVER')
        project = ms.getcol('PROJECT')
        schedule = ms.getcol('SCHEDULE_TYPE')
        telescope = ms.getcol('TELESCOPE_NAME')
        observer[0] = 'alan.loh@obspm.fr'
        project[0] = 'Fake Data'
        schedule[0] = 'NenuFAR'
        telescope[0] = 'NenuFAR'
        ms.putcol('OBSERVER', observer)
        ms.putcol('PROJECT', project)
        ms.putcol('SCHEDULE_TYPE', schedule)
        ms.putcol('TELESCOPE_NAME', telescope)
        ms.flush()
        ms.close()
        del observer, project, schedule, telescope, ms
        
        # SPECTRAL_WINDOW and DATA_DESCRIPTION tables
        # I think everything is fine here
        
        # FIELD and POINTING tables
        ms = table(
            tablename=join(self.msfile, 'POINTING'),
            ack=False,
            readonly=False
        )
        tracking = ms.getcol('TRACKING')
        tracking[...] = True
        ms.putcol('TRACKING', tracking)
        ms.flush()
        ms.close()
        del tracking, ms

        log.info(
            'OBSERVATION and POINTING tables updated.'
        )
        return


    def add_data_table(self, sources):
        """ Add the data related tables, seize opportunity to
            possibly simulate point sources.

            :param sources:
                Dictionnary like 
                {
                    'source1': {'ra': 0, 'dec': 0, 'flux': 1},
                    'source2': {'ra': 0, 'dec': 0, 'flux': 1}
                }
            :type sources:
                `dict`
        """
        na = np.newaxis
        ms = table(
            tablename=self.msfile,
            ack=False,
            readonly=False
        )
        # Get data from MS
        uvw = ms.getcol('UVW')
        data = ms.getcol('DATA')
        time = ms.getcol('TIME')
        desc = ms.getcol('DATA_DESC_ID')
        # Convert UVW in lambdas units
        msspw = table(
            tablename=join(self.msfile, 'SPECTRAL_WINDOW'),
            ack=False,
            readonly=True
        )
        chans = msspw.getcol('CHAN_FREQ')
        msspw.close()
        del msspw
        freq = np.take(
            chans,
            np.arange(self.nbands)[desc],
            axis=0
        ) # in Hz
        wavelength = const.c.value / freq
        uvw_l = uvw[:, na, :] / wavelength[..., na]
        # Loop over time, spw and sources
        # for time_stamp in np.unique(time):
        #     for spw_stamp in np.unique(desc):
        #         # Build selection mask
        #         selmask = (time == time_stamp)
        #         selmask *= (desc == spw_stamp)
        #         # Reinitialize everything to 0
        #         data[selmask, ...] = np.complex(0)
        #         # Construct fake visibilities
        #         for name in sources.keys():
        #             src = sources[name]
        #             data[selmask, ...] += add_src(
        #                 uvw=uvw_l[selmask, ...],
        #                 src_coord=(src['ra'], src['dec']),
        #                 flux=src['flux'],
        #                 phase_center=self.phase_center
        #             )[..., na]
        for name in sources.keys():
            src = sources[name]
            data += add_src(
                uvw=uvw_l,
                src_coord=(src['ra'], src['dec']),
                flux=src['flux'],
                phase_center=self.phase_center
            )[..., na]
        ms.putcol('CORRECTED_DATA', data)
        ms.flush()
        ms.close()
        del uvw, time, desc, data, ms
        return


    # --------------------------------------------------------- #
    # ----------------------- Internal ------------------------ #


# ============================================================= #

