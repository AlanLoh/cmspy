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

from casacore.tables import table
import os
from os.path import join
import numpy as np
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
        self.msfile = join(
            self.savepath,
            self.msname
        )


    # --------------------------------------------------------- #
    # --------------------- Getter/Setter --------------------- #


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
        # Fine as well        
        return


    def add_data_table(self):
        """ Add the data related tables, seie opportunity to
            possibly simulate point sources.
        """
        # TIME, DATA_DESC_ID, DATA
        ms = table(
            tablename=join(self.msfile),
            ack=False,
            readonly=False
        )
        uvw = ma.getcol('UVW')
        data = ms.getcol('DATA')
        time = ms.getcol('TIME')
        desc = ms.getcol('DATA_DESC_ID')
        for time_stamp in np.unique(time):
            for spw_stamp in np.unique(desc):
                selmask = (time == time_stamp)
                selmask *= (desc == spw_stamp)
                
                data[selmask, ...] = ...
        return


    # --------------------------------------------------------- #
    # ----------------------- Internal ------------------------ #


# ============================================================= #

