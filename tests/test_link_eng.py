#!/usr/bin/env python3
#
#   test_link_eng.py
#
#   Created - 29MAY23 - Kyle Eberhart
#
#------------------------------------------------------------------------------
import pytest
from link_engineering import link_eng as le
from link_engineering import units as u

sixGHz = u.Frequency(GHz=6.0)
fourGHz = u.Frequency(GHz=4.0)
geosync = u.Distance(km=40000)

def test_calc_noise_power_in_bandwidth():
    fiftyK = u.Temperature(k=50)
    thirtyMHz = u.Frequency(MHz=30.0)
    N = le.calc_noise_power_in_bandwidth(fiftyK, thirtyMHz)
    assert(N.dBw == pytest.approx(-136.8, 0.1))

def test_calc_power_received():
    p_tx = u.Power(dBw=8.0)
    g_tx = u.Gain(dB=24.0)
    g_rx = u.Gain(dB=44.0)
    freq = u.Frequency(GHz=4.0)
    rnge = u.Distance(km=40000.0)
    P_rx = le.calc_power_received(p_tx, g_tx, g_rx, freq, rnge)
    assert(P_rx.dBw == pytest.approx(-120, 0.2))

def test_calc_wavelength():
    wl = le.calc_wavelength(6000000000)
    assert(wl == pytest.approx(0.05, .01))

def test_calc_beamwidth():
    gain = u.Gain(dB=15.0)
    beamwidth = le.calc_beamwidth(gain)
    assert(beamwidth.degrees == pytest.approx(40.76, 0.2))

def test_calc_ant_G():
    diam = u.Distance(m=0.5)
    wl = u.Frequency(GHz=4.0)
    effiency = .60
    gain = le.calc_ant_G(effiency, diam, wl)
    assert(gain.dB == pytest.approx(24.0, 0.2))

def test_calc_half_power_beamwidth():
    diam = u.Distance(m=0.5)
    freq = u.Frequency(GHz=4.0)
    HPBW = le.calc_half_power_beamwidth(diam, freq)
    assert(HPBW.degrees == pytest.approx(10.5, 0.1))

def test_calc_effective_aperature():
    diam = u.Distance(m=.5)
    A_eff = le.calc_effective_aperature(.6, diam)
    assert(A_eff == pytest.approx(0.11, 0.08))

def test_calc_EIRP():
    gain = u.Gain(dB=15.0)
    pwr = u.Power(kW=10.0)
    EIRP = le.calc_EIRP(gain, pwr)
    assert(EIRP.kW == pytest.approx(316.2, .1))

def test_calc_free_space_loss():
    freq = u.Frequency(GHz=4.0)
    rnge = u.Distance(km=40000.0)
    fsl = le.calc_free_space_loss(rnge, freq)
    assert(fsl.dB == pytest.approx(196, 0.1))

