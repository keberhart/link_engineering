#!/usr/bin/env python3
#
#   test_link_eng.py
#
#   Created - 29MAY23 - Kyle Eberhart
#
#------------------------------------------------------------------------------
import pytest
import link_eng

def test_calc_beamwidth():
    beamwidth = link_eng.calc_beamwidth(15)
    assert pytest.approx(beamwidth, 0.2)
