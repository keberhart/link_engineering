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

def test_calc_SNR():
    """ Test the calc_SNR function
        Reference 3: Example 16.10.1 page 769
        Its a full link budget example, lots of test to run
        
        range = 36000 km
        u/l freq = 6 GHz
        d/l freq = 4 GHz
        et diam = 15 m
        sc diam = .5 m
        ant_eff = .60
        et pwr = 1 kW
        sc gain = 90 dB
        sc Tant = 300 k
        sc Tsys = 2700 k
        et Tant = 50 k
        et Tsys = 80 k
        bw = 30 MHz
    """
    rng = u.Distance(km=36000)
    ant_eff = .60
    et_diam = u.Distance(m=15)
    sc_diam = u.Distance(m=.5)
    et_pwr = u.Power(kW=1)
    sc_gain = u.Gain(dB=90)
    sc_Tsys = u.Temperature(k=2700)
    sc_Tant = u.Temperature(k=300)
    sc_Tsys = u.Temperature(k=2700)
    et_Tant = u.Temperature(k=50)
    et_Tsys = u.Temperature(k=80)
    bw = u.Frequency(MHz=30)
    # Calculate the wavelength
    ul_freq = u.Frequency(GHz=6.0)
    dl_freq = u.Frequency(GHz=4.0)
    assert(abs(ul_freq.wl - 0.05) < 0.01), f"Expected 0.05, got {ul_freq.wl}"
    assert(abs(dl_freq.wl - 0.075) < 0.001), f"Expected 0.075, got {dl_freq.wl}"
    # Calculate the free space loss for uplink and downlink
    fsl_u = le.calc_free_space_loss(rng, ul_freq)
    fsl_d = le.calc_free_space_loss(rng, dl_freq)
    assert(abs(fsl_u.dB - 199.13) < 0.01), f"Expected 199.13, got {fsl_u.dB}"
    assert(abs(fsl_d.dB - 195.61) < 0.01), f"Expected 195.61, got {fsl_d.dB}"
    # Calculate the antenna gains for uplink and downlink
    gain_te = le.calc_ant_G(ant_eff, et_diam, ul_freq)
    assert(abs(gain_te.dB - 57.27) < 0.01), f"Expected 57.27, got {gain_te.dB}"
    gain_rs = le.calc_ant_G(ant_eff, sc_diam, ul_freq)
    assert(abs(gain_rs.dB - 27.72) < 0.02), f"Expected 27.72, got {gain_rs.dB}"
    gain_ts = le.calc_ant_G(ant_eff, sc_diam, dl_freq)
    assert(abs(gain_ts.dB - 24.20) < 0.01), f"Expected 24.20, got {gain_ts.dB}"
    gain_re = le.calc_ant_G(ant_eff, et_diam, dl_freq)
    assert(abs(gain_re.dB - 53.75) < 0.01), f"Expected 53.75, got {gain_re.dB}"
    # calculate the transimit EIRP from the tx earth station
    p_te = le.calc_EIRP(gain_te, et_pwr)
    assert(abs(p_te.dBw - 87.27) < 0.01), f"Expected 87.27, got {p_te.dBw}"
    # calculate the power recieved by the spacecraft
    p_rs = u.Power(dBw=(p_te.dBw - fsl_u.dB + gain_rs.dB))
    assert(abs(p_rs.dBw - (-84.14)) < 0.01), f"Expected -84.14, got {p_rs.dBw}"
    # do that again, using one of the link engineering functions.
    p_rs_eng = le.calc_power_received(et_pwr, gain_te, gain_rs, ul_freq, rng)
    assert(abs(p_rs_eng.dBw - (-84.14)) < 0.01), f"Expected -84.14, got {p_rs_eng.dBw}"
    # calculate the transmit power of the spacecraft
    p_ts = u.Power(dBw=(sc_gain.dB + p_rs.dBw))
    assert(abs(p_ts.dBw - (5.86)) < 0.01), f"Expected 5.86, got {p_ts.dBw}"

    # calculate the EIRP of the spacecraft and the Earth station's receive power
    eirp_sc = le.calc_EIRP(gain_ts, p_ts)
    assert(abs(eirp_sc.dBw - (30.06)) < 0.02), f"Expected 30.6, got {eirp_sc.dBw}"
    p_re = u.Power(dBw=(eirp_sc.dBw - fsl_d.dB + gain_re.dB))
    assert(abs(p_re.dBw - (-111.80)) < 0.1), f"Expected -111.80, got {p_re.dBw}"

    # calculate the power received by the Earth station using the link engineering module
    p_re = le.calc_power_received(p_ts, gain_ts, gain_re, dl_freq, rng)
    assert(abs(p_re.dBw - (-111.80)) < 0.1), f"Expected -111.80, got {p_re.dBw}"
    # calculate the system noise temperatures
    t_rs = u.Temperature(k=(sc_Tant.k + sc_Tsys.k))
    t_re = u.Temperature(k=(et_Tant.k + et_Tsys.k))
    assert(abs(t_rs.k - (3000)) < 1), f"Expected 3000, got {t_rs.k}"
    assert(abs(t_re.k - (130)) < 1), f"Expected 130, got {t_re.k}"
    # calculate the noise power in the bandwidth of the system
    n_rs = le.calc_noise_power_in_bandwidth(t_rs, bw)
    n_re = le.calc_noise_power_in_bandwidth(t_re, bw)
    assert(abs(n_rs.dBw - (-119.06)) < 0.01), f"Expected -119.06, got {n_rs.dBw}"
    assert(abs(n_re.dBw - (-132.69)) < 0.01), f"Expected -132.69, got {n_re.dBw}"
    # calculate the G/T for the spacecraft and the earth station
    gt_rs = le.calc_G_T(gain_rs, t_rs)
    gt_re = le.calc_G_T(gain_re, t_re)
    assert(abs(gt_rs - (-7.05)) < 0.01), f"Expected -7.05, got {gt_rs}"
    assert(abs(gt_re - (32.61)) < 0.01), f"Expected 32.61, got {gt_re}"
    # calculate the SNR for the uplink and downlink
    snr_up = le.calc_SNR(p_te, fsl_u, gt_rs, bw)
    snr_dn = le.calc_SNR(eirp_sc, fsl_d, gt_re, bw)
    assert(abs(snr_up - (34.92)) < 0.01), f"Expected 34.92, got {snr_up}"
    assert(abs(snr_dn - (20.89)) < 0.01), f"Expected 20.89, got {snr_dn}"



    

