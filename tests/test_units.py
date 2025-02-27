#!/usr/bin/env python3
#
#   test_units.py
#
#   Created - 29MAY23 - Kyle Eberhart
#
#------------------------------------------------------------------------------
import pytest
from src.link_engineering import units

def test_frequency_Hz():
    freq = units.Frequency(Hz=1000)
    assert freq.Hz == 1000.0
    assert freq.KHz == 1.0
    assert freq.MHz == 0.001
    assert freq.GHz == 0.000001

def test_frequency_KHz():
    freq = units.Frequency(KHz=1.0)
    assert freq.Hz == 1000.0
    assert freq.KHz == 1.0
    assert freq.MHz == 0.001
    assert freq.GHz == 0.000001

def test_frequency_MHz():
    freq = units.Frequency(MHz=0.001)
    assert freq.Hz == 1000.0
    assert freq.KHz == 1.0
    assert freq.MHz == 0.001
    assert freq.GHz == 0.000001

def test_frequency_GHz():
    freq = units.Frequency(GHz=0.000001)
    assert freq.Hz == 1000.0
    assert freq.KHz == 1.0
    assert freq.MHz == 0.001
    assert freq.GHz == 0.000001
    assert freq.wl == 299792.458

def test_frequency_wl():
    freq = units.Frequency(wl=299792.458)
    assert freq.Hz == 1000.0
    assert freq.KHz == 1.0
    assert freq.MHz == 0.001
    assert freq.GHz == 0.000001
    assert freq.wl == 299792.458

def test_freq_repr():
    freq = units.Frequency(KHz=1.0)
    output = freq.__repr__()
    expected = '<Frequency 1e-06 GHz>'
    assert output == expected

def test_freq_wavelength():
    freq = units.Frequency(MHz=144.0)
    wl = units.Distance(m=2.0818)
    assert freq.wl == pytest.approx(wl.m, 0.002)

def test_distance_m():
    freq = units.Distance(m=1000.0)
    assert freq.m == 1000.0
    assert freq.km == 1.0
    assert freq.cm == 100000.0
    assert freq.mm == 1000000.0
    assert freq.au == 6.684587122268446e-09

def test_distance_km():
    freq = units.Distance(km=1.0)
    assert freq.m == 1000.0
    assert freq.km == 1.0
    assert freq.cm == 100000.0
    assert freq.mm == 1000000.0

def test_distance_cm():
    freq = units.Distance(cm=100000.0)
    assert freq.m == 1000.0
    assert freq.km == 1.0
    assert freq.cm == 100000.0
    assert freq.mm == 1000000.0

def test_distance_au():
    freq = units.Distance(au=1.0)
    assert freq.m == 149597870700.0

def test_distance_mm():
    freq = units.Distance(mm=1000000.0)
    assert freq.m == 1000.0
    assert freq.km == 1.0
    assert freq.cm == 100000.0
    assert freq.mm == 1000000.0

def test_dist_repr():
    freq = units.Distance(km=1.0)
    output = freq.__repr__()
    expected = '<Distance 1000.0 m>'
    assert output == expected

def test_power_W():
    power = units.Power(W=1.0)
    assert power.W == 1.0
    assert power.kW == .001
    assert power.mW == 1000.0
    assert power.dBw == 0.0
    assert power.dBm == 30.0

def test_power_kW():
    power = units.Power(kW=0.001)
    assert power.W == 1.0
    assert power.kW == .001
    assert power.mW == 1000.0
    assert power.dBm == 30.0

def test_power_mW():
    power = units.Power(mW=1000.0)
    assert power.W == 1.0
    assert power.kW == .001
    assert power.mW == 1000.0
    assert power.dBm == 30.0

def test_power_dBm():
    power = units.Power(dBm=30.0)
    assert power.W == 1.0
    assert power.kW == .001
    assert power.mW == 1000.0
    assert power.dBm == 30.0

def test_power_dBw():
    power = units.Power(dBw=0.0)
    assert power.W == 1.0
    assert power.kW == .001
    assert power.mW == 1000.0
    assert power.dBw == 0.0
    assert power.dBm == 30.0

def test_pwr_repr():
    freq = units.Power(W=1.0)
    output = freq.__repr__()
    expected = '<Power 1.0 W>'
    assert output == expected

def test_temp_k():
    power = units.Temperature(k=273.15)
    assert power.k == 273.15
    assert power.c == 0.0
    assert power.f == 32.0

def test_temp_c():
    power = units.Temperature(c=0.0)
    assert power.k == 273.15
    assert power.c == 0.0
    assert power.f == 32.0

def test_temp_f():
    power = units.Temperature(f=32.0)
    assert power.k == 273.15
    assert power.c == 0.0
    assert power.f == 32.0

def test_gain_amp():
    power = units.Gain(a=1.0)
    assert power.a == 1.0
    assert power.dB == 0.0

def test_gain_dB():
    power = units.Gain(dB=0.0)
    assert power.a == 1.0
    assert power.dB == 0.0

def test_gain_repr():
    freq = units.Gain(a=1.0)
    output = freq.__repr__()
    expected = '<Gain 1.0>'
    assert output == expected

def test_UnpackingError():
    value = units.Unit()
    with pytest.raises(units.UnpackingError):
        value.__iter__()

def test_GainValueError():
    with pytest.raises(ValueError):
        units.Gain()

def test_TemperatureValueError():
    with pytest.raises(ValueError):
        units.Temperature()

def test_PowerValueError():
    with pytest.raises(ValueError):
        units.Power()

def test_FrequencyValueError():
    with pytest.raises(ValueError):
        units.Frequency()

def test_DistanceValueError():
    with pytest.raises(ValueError):
        units.Distance()