#!/usr/bin/env python3
#
#   test_units.py
#
#   Created - 29MAY23 - Kyle Eberhart
#
#------------------------------------------------------------------------------
import pytest
from link_engineering import units

def test_frequency_Hz():
    errors = []
    freq = units.Frequency(Hz=1000)
    if not (freq.Hz == 1000.0):
        errors.append("Hz not correct value")
    if not (freq.KHz == 1.0):
        errors.append('KHz not corect value')
    if not (freq.MHz == 0.001):
        errors.append("MHz not correct value")
    if not (freq.GHz == 0.000001):
        errors.append("GHz not correct value")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_frequency_KHz():
    errors = []
    freq = units.Frequency(KHz=1.0)
    if not (freq.Hz == 1000.0):
        errors.append("Hz not correct value")
    if not (freq.KHz == 1.0):
        errors.append('KHz not corect value')
    if not (freq.MHz == 0.001):
        errors.append("MHz not correct value")
    if not (freq.GHz == 0.000001):
        errors.append("GHz not correct value")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_frequency_MHz():
    errors = []
    freq = units.Frequency(MHz=0.001)
    if not (freq.Hz == 1000.0):
        errors.append("Hz not correct value")
    if not (freq.KHz == 1.0):
        errors.append('KHz not corect value')
    if not (freq.MHz == 0.001):
        errors.append("MHz not correct value")
    if not (freq.GHz == 0.000001):
        errors.append("GHz not correct value")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_frequency_GHz():
    errors = []
    freq = units.Frequency(GHz=0.000001)
    if not (freq.Hz == 1000.0):
        errors.append("Hz not correct value")
    if not (freq.KHz == 1.0):
        errors.append('KHz not corect value')
    if not (freq.MHz == 0.001):
        errors.append("MHz not correct value")
    if not (freq.GHz == 0.000001):
        errors.append("GHz not correct value")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_freq_repr():
    freq = units.Frequency(KHz=1.0)
    errors = []
    output = freq.__repr__()
    expected = '<Frequency 1e-06 GHz>'
    if not(output == expected):
        errors.append('got: {}\nexpected: {}'.format(output, expected))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_freq_wavelength():
    errors = []
    freq = units.Frequency(MHz=144.0)
    wl = units.Distance(m=2.0818)
    if not (freq.wl == pytest.approx(wl.m, 0.002)):
        errors.append("{} calculated wl {} not {}".format(freq.Hz, freq.wl, wl.m))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_distance_m():
    errors = []
    freq = units.Distance(m=1000.0)
    if not (freq.m == 1000.0):
        errors.append("m not correct value")
    if not (freq.km == 1.0):
        errors.append('km not corect value')
    if not (freq.cm == 100000.0):
        errors.append("cm not correct value")
    if not (freq.mm == 1000000.0):
        errors.append("mm not correct value")
    if not(freq.au == 6.684587122268446e-09):
        errors.append("au not correct value: {}".format(freq.au))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_distance_km():
    errors = []
    freq = units.Distance(km=1.0)
    if not (freq.m == 1000.0):
        errors.append("m not correct value")
    if not (freq.km == 1.0):
        errors.append('km not corect value')
    if not (freq.cm == 100000.0):
        errors.append("cm not correct value")
    if not (freq.mm == 1000000.0):
        errors.append("mm not correct value")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_distance_cm():
    errors = []
    freq = units.Distance(cm=100000.0)
    if not (freq.m == 1000.0):
        errors.append("m not correct value")
    if not (freq.km == 1.0):
        errors.append('km not corect value')
    if not (freq.cm == 100000.0):
        errors.append("cm not correct value")
    if not (freq.mm == 1000000.0):
        errors.append("mm not correct value")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_distance_au():
    errors = []
    freq = units.Distance(au=1.0)
    if not (freq.m == 149597870700.0):
        errors.append("m not correct value")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_distance_mm():
    errors = []
    freq = units.Distance(mm=1000000.0)
    if not (freq.m == 1000.0):
        errors.append("m not correct value")
    if not (freq.km == 1.0):
        errors.append('km not corect value')
    if not (freq.cm == 100000.0):
        errors.append("cm not correct value")
    if not (freq.mm == 1000000.0):
        errors.append("mm not correct value")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_dist_repr():
    freq = units.Distance(km=1.0)
    errors = []
    output = freq.__repr__()
    expected = '<Distance 1000.0 m>'
    if not(output == expected):
        errors.append('got: {}\nexpected: {}'.format(output, expected))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_power_W():
    errors = []
    power = units.Power(W=1.0)
    if not (power.W == 1.0):
        errors.append("W not correct value")
    if not (power.kW == .001):
        errors.append('kWnot corect value')
    if not (power.mW == 1000.0):
        errors.append("mW not correct value")
    if not (power.dB == 0.0):
        errors.append("dB not correct value")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_power_kW():
    errors = []
    power = units.Power(kW=0.001)
    if not (power.W == 1.0):
        errors.append("W not correct value: {}".format(power.W))
    if not (power.kW == .001):
        errors.append('kWnot corect value: {}'.format(power.kW))
    if not (power.mW == 1000.0):
        errors.append("mW not correct value: {}".format(power.mW))
    if not (power.dB == 0.0):
        errors.append("dB not correct value: {}".format(power.dB))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_power_mW():
    errors = []
    power = units.Power(mW=1000.0)
    if not (power.W == 1.0):
        errors.append("W not correct value: {}".format(power.W))
    if not (power.kW == .001):
        errors.append('kWnot corect value: {}'.format(power.kW))
    if not (power.mW == 1000.0):
        errors.append("mW not correct value: {}".format(power.mW))
    if not (power.dB == 0.0):
        errors.append("dB not correct value: {}".format(power.dB))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_power_dB():
    errors = []
    power = units.Power(dB=0.0)
    if not (power.W == 1.0):
        errors.append("W not correct value: {}".format(power.W))
    if not (power.kW == .001):
        errors.append('kW not corect value: {}'.format(power.kW))
    if not (power.mW == 1000.0):
        errors.append("mW not correct value: {}".format(power.mW))
    if not (power.dB == 0.0):
        errors.append("dB not correct value: {}".format(power.dB))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_pwr_repr():
    freq = units.Power(W=1.0)
    errors = []
    output = freq.__repr__()
    expected = '<Power 1.0 W>'
    if not(output == expected):
        errors.append('got: {}\nexpected: {}'.format(output, expected))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))
