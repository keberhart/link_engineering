#!/usr/bin/env python3
''' Test the operation of the calc_antenna_T function
'''
from link_engineering import link_eng as le
from link_engineering import units as u


# define our antenna system
effective_aperature = 500.0
gain = le.calc_ant_G()
beamwidth = le.calc_beamwidth()