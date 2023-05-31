#!/usr/bin/env python3
''' Test the operation of the calc_antenna_T function
'''
from link_engineering import link_eng as le
from link_engineering import units as u


# define our antenna system
diam = u.Distance(m=30.157)
ant_eff = 0.7
wl = u.Frequency(wl=.020)
print(wl)
gain = le.calc_ant_G(ant_eff, diam, wl)
beamwidth = le.calc_beamwidth(gain)
