#!/usr/bin/env python3
#
#   test_link_eng.py
#
#   Created - 29MAY23 - Kyle Eberhart
#
#------------------------------------------------------------------------------
import pytest
from src.link_engineering import link_eng as le
from src.link_engineering import units as u

sixGHz = u.Frequency(GHz=6.0)
fourGHz = u.Frequency(GHz=4.0)
geosync = u.Distance(km=40000)

def test_calc_noise_power_in_bandwidth():
    """Test calculation of noise power in a bandwidth.
        N = k*T*B
        where N is noise power in dBw, k is Boltzmann's constant (1.38e-23 J/K),
              T is temperature in Kelvin, and B is bandwidth in Hz.
        reference 3: page 755, equation 16.7.1
        reference 3: page 756, example 16.7.1

        T = 50 K
        B = 30 MHz

    """
    fiftyK = u.Temperature(k=50)
    thirtyMHz = u.Frequency(MHz=30.0)
    N = le.calc_noise_power_in_bandwidth(fiftyK, thirtyMHz)
    assert(abs(N.dBw - (-136.8)) < 0.1), f"expected -136.8 dBW, got {N.dBw} dBW"

def test_calc_power_received():
    """Test calculation of power received at the receiver.
        P_rx = P_tx + G_tx - free_space_loss + G_rx
 
        where P_rx is power received in dBw, P_tx is power transmitted in dBw, G_tx and G_rx are gains in dB, free_space_loss is in dB.
        range is in km, uses units.Distance object
        frequency is in GHz, uses units.Frequency object

        reference 3: page 754, equation 16.6.7
        reference 3: page 754, example 16.6.1
    """
    p_tx = u.Power(dBw=8.0)
    g_tx = le.calc_ant_G(.60, u.Distance(m=0.5), u.Frequency(GHz=4.0))
    assert(abs(g_tx.dB - 24.2) < 0.1), f"expected 24 dB, got {g_tx.dB} dB"
    g_rx = le.calc_ant_G(.60, u.Distance(m=5.0), u.Frequency(GHz=4.0))
    assert(abs(g_rx.dB - 44.2) < 0.1), f"expected 44 dB, got {g_rx.dB} dB"
    freq = u.Frequency(GHz=4.0)
    rnge = u.Distance(km=40000.0)
    P_rx = le.calc_power_received(p_tx, g_tx, g_rx, freq, rnge)
    assert(abs(P_rx.dBw - (-120)) < 0.2), f"expected -120 dBW, got {P_rx.dBw} dBW"

def test_calc_wavelength():
    wl = le.calc_wavelength(6000000000)
    assert(wl == pytest.approx(0.05, .01))

def test_calc_beamwidth():
    """Test beamwidth calculation.
        Example 16.2.2 page 744
        G = 15 dB
        beamwidth = 40.76 degrees

    """
    gain = u.Gain(dB=15.0)
    beamwidth = le.calc_beamwidth(gain)
    assert(abs(beamwidth.degrees - 40.76) < .02), f"Expected beamwidth of 40.76 degrees, got {beamwidth.degrees}"

def test_calc_ant_G():
    """Test antenna gain calculation.
        reference 3: Example 16.6.1 page 754
        effiency = .60
        diameter = 0.5 m
        frequency = 4 GHz
        G = 24 dB
    """
    diam = u.Distance(m=0.5)
    freq = u.Frequency(GHz=4.0)
    effiency = .60
    gain = le.calc_ant_G(effiency, diam, freq)
    assert(abs(gain.dB - 24.2) < .1), f"Expected gain of 24 dB, got {gain.dB}"

def test_calc_half_power_beamwidth():
    """Test half power beamwidth calculation.
        reference 3: page 748; equation 16.3.11
        diameter of the parabolic reflector in meters, units.Distance object
        wavelength is in meters, uses units.Frequency object
        HPBW is in degrees, units.Angle object

        reference 3; page 748; equation 16.3.11
        reference 3; page 748; example 16.3.3

        diam = 0.5 m
        freq = 4 GHz
    """
    diam = u.Distance(m=0.5)
    freq = u.Frequency(GHz=4.0)
    HPBW = le.calc_half_power_beamwidth(diam, freq)
    assert(abs(HPBW.degrees - 10.5) < 0.1), f"Expected HPBW of 10.5 degrees, got {HPBW.degrees}"

def test_calc_effective_aperature():
    """Test effective aperature calculation.
       reference 3; page 748; equation 16.3.8
       diameter of the parabolic reflector in meters, units.Distance object
       antenna_effiency is a decimal percentage
       Returns a float(m^2)

        diam = 0.5 m
        effiency = 60%

        The reference doesn't solve for the effective aperature, but it does provide an example that uses this equation to solve for Gain.
    """
    diam = u.Distance(m=.5)
    A_eff = le.calc_effective_aperature(.6, diam)
    assert(abs(A_eff - 0.1178) < 0.001), f"Expected effective aperature of 0.1178 m^2, got {A_eff}"

def test_calc_EIRP():
    """Test EIRP calculation.
        from reference 3: example 16.2.1 page 743
        EIRP = 10 kW, gain = 15 dB
    """
    gain = u.Gain(dB=15.0)
    pwr = u.Power(kW=10.0)
    EIRP = le.calc_EIRP(gain, pwr)
    assert(abs(EIRP.kW - 316.2) < 0.1), f"Expected EIRP of 316.2 kW, got {EIRP.kW}"

def test_calc_free_space_loss():
    """Test Free Space Loss calculation.
        from reference 3: example 16.6.1 page 754
        FSL = (4*pi*range/wavelength)^2
        range is a units.Distance
        wavelength is a units.Frequency
        FSL is in dB

        freq = 4 GHz
        range is 40,000 km
    """
    freq = u.Frequency(GHz=4.0)
    rnge = u.Distance(km=40000.0)
    fsl = le.calc_free_space_loss(rnge, freq)
    assert(abs(fsl.dB - 196.5) < 0.1), f"Expected FSL of 196 dB, got {fsl.dB}"

def test_calc_volts_meters():
    flux_density = u.Power(W=9.0)
    volts_per_meter = le.calc_volts_meters(flux_density)
    assert(abs(volts_per_meter - 58.2) <= 0.1), f"Expected 58.2, got {volts_per_meter}"

def test_flux_density():
    """Test the calculation of flux density.
        from reference 3: example 16.2.1 page 743
        EIRP = 10 kW, gain = 15 dB, range = 5 km
        Flux density at range of 5 km should be .001 W/m^2
        or 0.62 v/m^2
    """
    tx_pwr = u.Power(kW=10.0)
    tx_g = u.Gain(dB=15.0)
    EIRP = le.calc_EIRP(tx_g, tx_pwr)
    assert(abs(EIRP.kW - 316.2) <= .5), f"Expected 316.2, got {EIRP.kW}"
    rng = u.Distance(km=5)
    flux = le.calc_Flux_Density(EIRP, rng)
    assert(abs(flux.W - 0.001) <= .00005), f"Expected 0.001, got {flux.W}"
    vm = le.calc_volts_meters(flux)
    assert(abs(vm - 0.62) <= 0.05), f"Expected 0.62, got {vm}"

def test_sefd():
    # having trouble getting this to work. Found several example
    #   data sets on the web, but none come out as close as I would hope.
    # from the LWA:
    # examples used: Ae = 800, Tsys=1260, sefd=4370
    # examples used: Ae = 1020, Tsys=1740, sefd=4680
    # from Google Gemini: but Gemini does math bad and the sefd out was off
    # example used: Ae = 100, Tsys=100, ~sefd=2760.6
    A_eff = 100.0
    T_sys = u.Temperature(k=100.0)
    SEFD = le.calc_SEFD(A_eff, T_sys)
    assert SEFD == pytest.approx(2760.6, .01)
    assert(SEFD == pytest.approx(2760.6, .01))

def test_antenna_t():
    # example from the McMaster University slides:
    #Example (modified from Kraus, p. 406): A circular reflector antenna of
    # 500 m2 effective aperture operating at λ = 20 cm is directed at the
    # zenith. What is the total antenna temperature assuming the sky
    # temperature close to zenith is equal to 10° K, whereas at the horizon it
    # is 150° K? Take the ground temperature equal to 300° K and assume that
    # one-half of the minor-lobe beam is in the backdirection (toward the
    # ground) and one-half is toward the horizon. The main beam efficiency is
    # BEM =0.7.

    ant_diam = u.Distance(m=500)
    # example is an area not diam? why is this working?
    ant_eff = 0.7
    wl = u.Frequency(wl=20)
    beamwidth = le.calc_beamwidth(le.calc_ant_G(ant_eff, ant_diam, wl))
    sky_temp_k = u.Temperature(k=10)
    ambient_temp_k = u.Temperature(k=300)
    T = le.calc_antenna_T(beamwidth, ant_eff, sky_temp_k, ambient_temp_k)
    assert T.k == pytest.approx(74.5, .01)

def test_NF_and_T():
    # Noise Figure = 6 dB
    # Temperature K = 870
    NF = 6
    T = le.NF_to_T_noise(NF)
    assert T == pytest.approx(864.5, .1)
    T = 870
    NF = le.T_noise_to_NF(T)
    assert NF == pytest.approx(6.02, .01)