#!/usr/bin/env python3
#
#   test_link_eng.py
#
#   Created - 29MAY23 - Kyle Eberhart
#
#------------------------------------------------------------------------------
import pytest
from link_engineering import link_eng as le

def test_calc_wavelength():
    wl = le.calc_wavelength(6000000000)
    assert(wl == pytest.approx(0.05, .01))

def test_calc_beamwidth():
    beamwidth = le.calc_beamwidth(15)
    assert(beamwidth == pytest.approx(40.76, 0.2))

def test_calc_ant_G():
    gain = le.calc_ant_G(.60, 0.5, le.calc_wavelength(4000000000))
    assert(gain == pytest.approx(24.0, 0.2))

def test_calc_half_power_beamwidth():
    HPBW = le.calc_half_power_beamwidth(le.calc_wavelength(4000000000), 0.5)
    assert(HPBW == pytest.approx(10.5, 0.1))

def test_calc_effective_aperature():
    A_eff = le.calc_effective_aperature(.5, .6)
    assert(A_eff == pytest.approx(0.11, 0.08))

def test_calc_EIRP():
    EIRP = le.calc_EIRP(15.0, 10)
    assert(EIRP == pytest.approx(316.2, .1))

def test_calc_free_space_loss():
    fsl = le.calc_free_space_loss(4000000000, 40000000)
    assert(fsl == pytest.approx(196, 0.1))

def test_calc_power_received():
    P_rx = le.calc_power_received(8.0, 24, 44, 4000000000, 400000000)
    assert(P_rx == pytest.approx(-120, 0.2))