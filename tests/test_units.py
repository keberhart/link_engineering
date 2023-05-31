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
        errors.append("Hz not correct value: {}".format(freq.Hz))
    if not (freq.KHz == 1.0):
        errors.append('KHz not corect value: {}'.format(freq.KHz))
    if not (freq.MHz == 0.001):
        errors.append("MHz not correct value: {}".format(freq.MHz))
    if not (freq.GHz == 0.000001):
        errors.append("GHz not correct value: {}".format(freq.GHz))
    if not (freq.wl == 299792.458):
        errors.append("wl no correct value: {}".format(freq.wl))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_frequency_wl():
    errors = []
    freq = units.Frequency(wl=299792.458)
    if not (freq.Hz == 1000.0):
        errors.append("Hz not correct value: {}".format(freq.Hz))
    if not (freq.KHz == 1.0):
        errors.append('KHz not corect value: {}'.format(freq.KHz))
    if not (freq.MHz == 0.001):
        errors.append("MHz not correct value: {}".format(freq.MHz))
    if not (freq.GHz == 0.000001):
        errors.append("GHz not correct value: {}".format(freq.GHz))
    if not (freq.wl == 299792.458):
        errors.append("wl no correct value: {}".format(freq.wl))
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
        errors.append("W not correct value: {}".format(power.W))
    if not (power.kW == .001):
        errors.append('kWnot corect value: {}'.format(power.kW))
    if not (power.mW == 1000.0):
        errors.append("mW not correct value: {}".format(power.mW))
    if not (power.dBw == 0.0):
        errors.append("dBw not correct value: {}".format(power.dBw))
    if not (power.dBm == 30.0):
        errors.append("dBm not correct value: {}".format(power.dBm))
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
    if not (power.dBm == 30.0):
        errors.append("dBm not correct value: {}".format(power.dBm))
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
    if not (power.dBm == 30.0):
        errors.append("dBm not correct value: {}".format(power.dBm))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_power_dBm():
    errors = []
    power = units.Power(dBm=30.0)
    if not (power.W == 1.0):
        errors.append("W not correct value: {}".format(power.W))
    if not (power.kW == .001):
        errors.append('kW not corect value: {}'.format(power.kW))
    if not (power.mW == 1000.0):
        errors.append("mW not correct value: {}".format(power.mW))
    if not (power.dBm == 30.0):
        errors.append("dBm not correct value: {}".format(power.dBm))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_power_dBw():
    errors = []
    power = units.Power(dBw=0.0)
    if not (power.W == 1.0):
        errors.append("W not correct value: {}".format(power.W))
    if not (power.kW == .001):
        errors.append('kW not corect value: {}'.format(power.kW))
    if not (power.mW == 1000.0):
        errors.append("mW not correct value: {}".format(power.mW))
    if not (power.dBw == 0.0):
        errors.append("dBw not correct value: {}".format(power.dBw))
    if not (power.dBm == 30.0):
        errors.append("dBm not correct value: {}".format(power.dBm))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_pwr_repr():
    freq = units.Power(W=1.0)
    errors = []
    output = freq.__repr__()
    expected = '<Power 1.0 W>'
    if not(output == expected):
        errors.append('got: {}\nexpected: {}'.format(output, expected))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_temp_k():
    errors = []
    power = units.Temperature(k=273.15)
    if not (power.k == 273.15):
        errors.append("K not correct value: {}".format(power.k))
    if not (power.c == 0.0):
        errors.append('C not corect value: {}'.format(power.c))
    if not (power.f == 32.0):
        errors.append("f not correct value: {}".format(power.f))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_temp_c():
    errors = []
    power = units.Temperature(c=0.0)
    if not (power.k == 273.15):
        errors.append("K not correct value: {}".format(power.k))
    if not (power.c == 0.0):
        errors.append('C not corect value: {}'.format(power.c))
    if not (power.f == 32.0):
        errors.append("f not correct value: {}".format(power.f))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_temp_f():
    errors = []
    power = units.Temperature(f=32.0)
    if not (power.k == 273.15):
        errors.append("K not correct value: {}".format(power.k))
    if not (power.c == 0.0):
        errors.append('C not corect value: {}'.format(power.c))
    if not (power.f == 32.0):
        errors.append("f not correct value: {}".format(power.f))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_pwr_repr():
    freq = units.Temperature(k=1.0)
    errors = []
    output = freq.__repr__()
    expected = '<Temperature 1.0 K>'
    if not(output == expected):
        errors.append('got: {}\nexpected: {}'.format(output, expected))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_gain_amp():
    errors = []
    power = units.Gain(a=1.0)
    if not (power.a == 1.0):
        errors.append("a not correct value: {}".format(power.a))
    if not (power.dB == 0.0):
        errors.append('dB not corect value: {}'.format(power.dB))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_gain_dB():
    errors = []
    power = units.Gain(dB=0.0)
    if not (power.a == 1.0):
        errors.append("a not correct value: {}".format(power.a))
    if not (power.dB == 0.0):
        errors.append('dB not corect value: {}'.format(power.dB))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_gain_repr():
    freq = units.Gain(a=1.0)
    errors = []
    output = freq.__repr__()
    expected = '<Gain 1.0>'
    if not(output == expected):
        errors.append('got: {}\nexpected: {}'.format(output, expected))
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

