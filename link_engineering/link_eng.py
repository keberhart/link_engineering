#!/usr/bin/env python3
#
#   A library for satellite link engineering equations.
#
#   Kyle Eberhart - 29OCT20
#
#   Public Domain - no implied warranty, use at your own risk
#
#   1. This library uses many of the ideas and equations from;
#       "Link Performance Analysis for a Proposed Future Architecture of the
#       Air Force Satellite Control Network" by Eric W. Nelson, USAF
#
#   2. Just like Cpt. Nelson I also referenced;
#       "DSN Telecommunications Link Design Handbook" 810-005 rev. E
#
#   3. I have also used;
#       "Electromagnetic Waves and Antennas" by Sophocles J. Orfanidis
#
#   4. Noise figure calculations and antenna effective aperature were taken
#       from the source code of "Virgo: A Versatile Spectrometer for Radio
#       Astronomy" by Apostolos Spanakis-Misirlis, Cameron L. Van Eck and
#       E.p. Boven
#
#   5. "Antenna Models For Electromagnetic Compatability Analyses"
#           NTIA TM-12-489, C.W Wang Ph.D., T. Keech, Ph.D.
#
# -----------------------------------------------------------------------------

import math
from scipy.special import jv
from scipy.special import erfc
from link_engineering.constants import K, K_dBW, C, ERAD
from link_engineering import units

def calc_noise_power_in_bandwidth(temperature, bandwidth):
    '''Average power in Watts

        N = k*temperature*bandwidth

        where k is boltzmanns constant
        where temperature is in K
        where bandwidth is in Hz

        returns noise power in dB
    '''
    _N = K*temperature*bandwidth
    _N = lin_to_db(_N)
    return _N

def calc_SNR(EIRP, L, GoT):
    '''Signal to Noise Ratio

        (C/No) = (EIRP)*(1/L)*(GoT)*(1/k)

        EIRP is the Effective Isotropic Radiated Power in dB
        L is the medium losses in dB
        GoT is the receiving system G/T or System Gain over System noise
            temperature.
        k is Boltzmann's constant (1.3806x10^-23 J/K or -228.5991 dBW/K/Hz)

    '''
    _SNR = (EIRP)*(1/L)*(GoT)*(1/K)
    return _SNR

def calc_power_received(P_tx, G_tx, G_rx, frequency, range):
    '''Power received at the distant end, with free space losses

        P_rx = P_tx*G_tx*((wavelength/(3*pi*range))^2)*G_rx

        P_tx is in dB
        G_tx is in dB
        G_rx is in dB
        wavelength is in m
        range is in m

        returns power received in dB

    '''
    P_rx = P_tx + G_tx - calc_free_space_loss(range, frequency) + G_rx
    return P_rx

def calc_EIRP(G, P):
    '''Effective Isotropic Radiated Power

        EIRP = G*P

        G is the Gain of the transmit antenna in dB
        P is the radiated power, output will be in the same units used as the input. ie: watts in watts out, kW in kW out, mW in mW out.

    '''
    G = math.pow(10, G/10)
    _EIRP = G*P
    return _EIRP


def calc_wavelength(freq):
    '''Wavelength

        wave_length = c/freq

        c is the speed of light in m/s
        freq is the frequency in Hz

    '''
    wavelength = C/freq
    return wavelength


def calc_ant_G(antenna_effiency, diameter, wavelength):
    '''Gain of a simple prime focus parbolic antenna

        G = antenna_effiency*(pi()*diameter/wavelength)^2

        antenna_effiency is a decimal percentage
        diameter is in m
        wavelength is in m

    '''
    _G = antenna_effiency*math.pow(math.pi*diameter/wavelength, 2)
    return 10*math.log(_G, 10)


def calc_effective_aperature(diameter, antenna_effiency):
    '''Antenna effective aperature [m^2]

        A_eff = antenna_effiency*(1/4)*pi()*diameter^2
        
        diameter is in m
        antenna_effiency is a decimal percentage

    '''
    A_eff = antenna_effiency * (1/4) * math.pi * math.pow(diameter, 2)
    return A_eff


def calc_beamwidth(G):
    '''Antenna beamwidth in degrees

        G is antenna gain in dB, calculated above...

    '''
    G = math.pow(10, G/10)
    _beamwidth = math.sqrt(16/G)
    return math.degrees(_beamwidth)


def calc_half_power_beamwidth(wavelength, diameter):
    '''3dB beamwidth or HPBW

        reference 3; page 748; equation 16.3.11
        "The constant 70 degrees represents only a rough approximation..."

        HPBW = 70*(wavelength/diameter)

        diameter of the parabolic reflector in meters
        wavelength is the wavelength in meters

    '''
    _HPBW = 70*wavelength/diameter
    return _HPBW


def calc_antenna_T(beamwidth, antenna_effiency, sky_temp_K, ambient_temp_K):
    '''Antenna Temperature

        beamwidth of the antenna at frequency
        antenna_effiency is a decimal percentage
        sky_temp_K is the sky temperature in Kelvin, varies per frequency
        ambient_temp_K is the ambient temperature in Kelvin

        I am not sure where I got this equation/function. It has parts that
        look similar to things in reference 3, at the end of page 758.

        I would like to update this to better account for frequency and
        elevation angle. Reference 2 has several interesting equations but
        will require quite a bit of work to get things working.

    '''
    Ta_mb = 1/beamwidth*(sky_temp_K*(antenna_effiency)*beamwidth)
    Ta_gbl = 1/beamwidth*(ambient_temp_K*(1-antenna_effiency)/2*beamwidth)
    Ta_hbl = 1/beamwidth*(ambient_temp_K/2*(1-antenna_effiency)/2*beamwidth)
    _T = Ta_mb + Ta_gbl + Ta_hbl
    return _T


def calc_G_T(G, T_sys):
    '''Calculate the antenna G/T

        G is the antenna gain in dBi
        T_sys is the antten noise temperature in K

    '''
    _G_T = G-lin_to_db(T_sys)
    return _G_T


def NF_to_T_noise(NF, T_ref=290):
    '''Convert Noise Figure to noise temperature [K]

        NF is Noise Figure in dB
        T_ref is the reference temperature in K

    '''
    _T_noise = T_ref*((10**(NF/10)) - 1)
    return _T_noise


def T_noise_to_NF(T_noise, T_ref=290):
    '''Convert a noie temperature to NF [dB]

        T_noise is the noise temperature in K
        T_ref is the reference temperature in K

    '''
    _NF = lin_to_db((T_noise/T_ref) + 1)
    return _NF


def calc_SEFD(eff_aperature, T_sys):
    '''System Equivilent flux density [Jy]

        eff_aperature is the antenna effective aperature in m^2
        T_sys is the system noise temperature in [K]

    '''
    _sefd = 10**26 * 2*K*T_sys/eff_aperature
    return _sefd


def calc_radiometer_equation(S_flux, sefd, on_time, bw):
    '''Estimate the snr for an observation

        S_flux is the source flux density in Jy
        sefd is the system equivalent flux density in Jy
        on_time is the on source integration time in seconds
        bw is the aquisition bandwidth in Hz

    '''
    _snr = S_flux*math.sqrt(on_time*bw)/sefd
    return _snr


def calc_off_nadir(el_angle, sc_alt, gs_alt):
    '''Angle off of earth pointng beam

        elevation angle of the ground station antenna
        spacecraft altitude in meters
        ground station altitude in meters

    '''
    gs_part = (gs_alt+ERAD)*math.sin(math.radians(el_angle+90.0))
    _DOFF = math.degrees(math.asin(gs_part/(sc_alt+ERAD)))
    return _DOFF


def calc_pointing_loss(point_err, HPBW):
    '''Pointing error loss

        point_err is the pointing offset error in degrees
        HPBW is the half power beamwidth of the antenna in degrees

    '''
    print("doesn't work right!")
    loss1 = 3*math.pow(point_err/HPBW, 2)
    loss2 = -12*math.pow(point_err/HPBW, 2)
    loss3 = 0.063*(math.pow(point_err, 2)/math.pow(HPBW, 2))
    _Point_loss = (10*math.log(
                        math.exp(
                            2.773*math.pow(
                                point_err, 2)/math.pow(HPBW, 2))))
    return _Point_loss, loss1, loss2, loss3


def calc_atmo_loss(el_angle):
    '''A rough estimate for atmospheric loss. There are much better ways
        to do this, but this is very easy.

    '''
    _atmo_loss = 1+(1/el_angle)
    return lin_to_db(_atmo_loss)


def calc_free_space_loss(slant_range, frequency):
    '''Free Space Loss

        FSL = (4*pi*range*frequency/c)^2

        slant_range is the straight line distance to the spacecraft from
            the earth terminal in meters
        frequency is in Hz
        c is the speed of light in m/s

    '''
    _FSL = math.pow(4*math.pi*slant_range*frequency/C, 2)
    return lin_to_db(_FSL)


def calc_polarization_loss(nadir_off):
    '''Polarization Loss

        Lpol = 1.389*10^8(nadir_off^4)-3.389*10^4(nadir_off^2)-2.86*10^7 (dB)

        nadir_off is radians offset from boresight

    '''
    print("doesn't work right!")
    _Lpol = 1.389*math.pow(
            10, -8)*math.pow(
                    nadir_off, 4)-3.389*math.pow(
                        10, -4)*math.pow(
                                nadir_off, 2)-2.286*math.pow(10, -7)
    return _Lpol


def uplink_performance(EIRP, uplink_loss, GoTsc, k):
    '''Uplink performance

        (C/No)uplink = (EIRPground_station)(1/uplink_loss)(G/Tsc)(1/k)

        EIRPground_station is the EIRP from the ground station
        uplink_loss is the total uplink losses in dB
        k is Boltzmann's constant

    '''
    _CoNo = EIRP*(1/uplink_loss)*(GoTsc)*(1/k)
    return _CoNo


def downlink_performance(EIRP, downlink_loss, GoTgs, k):
    '''Downlink performance

        (C/No)downlink = (EIRPsc)*(1/downlink_loss)*(GoTgs)*(1/k)

        EIRPsc is the EIRP from the spacecraft
        downlink_loss is the total downlnk losses in dB
        k is Boltzmann's constant

    '''
    _CoNo = EIRP*(1/downlink_loss)*(GoTgs)*(1/k)
    return _CoNo


def service_mod_loss(mod_index):
    '''Service Modulation loss

        service_mod_loss = 10*log10(2*bessel(1, mod_index)^2)

        mod_index is the modulation index of the subcarrier
        bessel is the bessel function of the first order

    '''
    _service_mod_loss = 10*math.log(2*math.pow(jv(1, mod_index), 2))
    return _service_mod_loss


def TLM_EbNo(CoNoTLM, service_mod_loss, data_rate_loss):
    '''Eb/No of the telemetry stream

        CoNoTLM is C/No of the data stream
        service_mod_loss is the loss due to modulation
        data_rate_loss is the losses due to the datarate changes

    '''
    _TLM_EbNo = CoNoTLM-service_mod_loss-data_rate_loss
    return _TLM_EbNo


def bit_error_rate(TLM_EbNo):
    '''Bit Error Rate - if it is an SGLS waveform

        BER = 0.5*erfc(sqrt(TLM_EbNo)

        erfc is the complimentary error function
        TLM_EbNo is the telemetry subcarrier engergy per bit over noise
            density in dB

    '''
    _BER = 0.5*erfc(math.sqrt(TLM_EbNo))
    return _BER


def lin_to_db(value):
    '''Convert a value from linear form to logrithmic dB
    '''
    result = 10*math.log10(value)
    return result


def db_to_lin(value):
    '''Convert a value from dB to linear form
    '''
    result = math.pow(10, value/10)
    return result


def S_surface(power, diameter):
    ''' The maximum power density in front of an antenna, at the surface.

        power is the the input power in Watts
        diameter is the antenna diameter in meters

        From: Federal Communications Commission: Office of Engineering &
            Technology, Evaluating Compliance with FCC Guidelines for Human
            Exposure to Radiofrequency Electromagnetic Fields, 1997.

            Equation 11
    '''
    area = math.pi*math.pow(diameter/2, 2)
    result = (4 * power) / area
    return result


def R_nf(diameter, wavelength):
    ''' The extent of the near-field or Fresnel region.

        diameter is the antenna diameter in meters
        wavelength in meters

        From: Federal Communications Commission: Office of Engineering &
            Technology, Evaluating Compliance with FCC Guidelines for Human
            Exposure to Radiofrequency Electromagnetic Fields, 1997.

            Equation 12
    '''
    result = math.pow(diameter, 2)/(4*wavelength)
    return result


def S_nf(ant_efficiency, power, diameter):
    ''' The maximum near-field, on axis, power density.

        ant_efficiency is eta aperature efficiency, usually 0.5-0.75
        power is the power fed to the antenna in Watts
        diameter is the antenna diameter in meters

        From: Federal Communications Commission: Office of Engineering &
            Technology, Evaluating Compliance with FCC Guidelines for Human
            Exposure to Radiofrequency Electromagnetic Fields, 1997.

            Equation 13
    '''
    result = (16*ant_efficiency*power)/(math.pi*math.pow(diameter, 2))
    return result


def R_ff(diameter, wavelength):
    ''' The range or distance to the beginning of the far-field.

        diameter is the antenna diameter in meters
        wavelength of our transmit signal in meters

        From: Federal Communications Commission: Office of Engineering &
            Technology, Evaluating Compliance with FCC Guidelines for Human
            Exposure to Radiofrequency Electromagnetic Fields, 1997.

            Equation 16
    '''
    result = (0.6*math.pow(diameter, 2))/wavelength
    return result


def S_t(S_nf, R_nf, R):
    ''' Power density for range R in the transition region, between R_nf and R_ff.

        S_nf is power density in W/m^2
        R_nf is the extent of the near-field in meters
        R is the distance to the point of interest in meters

        From: Federal Communications Commission: Office of Engineering &
            Technology, Evaluating Compliance with FCC Guidelines for Human
            Exposure to Radiofrequency Electromagnetic Fields, 1997.

            Equation 17
    '''
    result = (S_nf*R_nf)/R
    return result


def S(EIRP, R):
    ''' Power density for range R in the far-field.

        EIRP is the Effective Isotropic Radiated Power in Watts
        R is the distance to the point of interest in meters

        From: Federal Communications Commission: Office of Engineering &
            Technology, Evaluating Compliance with FCC Guidelines for Human
            Exposure to Radiofrequency Electromagnetic Fields, 1997.

            Equation 4
    '''
    result = EIRP/(4*math.pi*math.pow(R, 2))
    return result


def S_worst(EIRP, R):
    ''' Worst case power density at or near a surface, 100% reflection

        EIRP is the Effective Isotropic Radiated Power in Watts
        R is the distance to the point of interest in meters

        From: Federal Communications Commission: Office of Engineering &
            Technology, Evaluating Compliance with FCC Guidelines for Human
            Exposure to Radiofrequency Electromagnetic Fields, 1997.

            Equation 6
    '''
    result = EIRP/(math.pi*math.pow(R, 2))
    return result


def statgain(G_max, phi):
    '''Statgain default High-gain radiation pattern model for antennas
        with G_max >= 10 dBi

        G_max is antenna gain in dB
        phi is the angle off of the mainbeam axis
    '''
    phi_m = (50*(0.25*G_max+7)**0.5)/(10**(G_max/20.0))
    phi_r1 = 27.466*10**(-0.3*G_max/10)
    phi_r2 = 250/(10**(G_max/20))
    phi_r3 = phi_r2
    phi_b1 = 48
    phi_b2 = phi_b1
    phi_b3 = 131.8257*10**(-1*G_max/50)

    if (G_max >= 48):
        if (0 <= phi <= phi_m):
            return G_max-4*10**(-4)*(10**(G_max/10))*phi**2
        if (phi_m < phi <= phi_r1):
            return 0.75*G_max-7
        if (phi_r1 < phi <= phi_b1):
            return 29-25*math.log(phi)
        if (phi_b1 < phi <= 180):
            return -13
    if (22 <= G_max < 48):
        if (0 <= phi <= phi_m):
            return G_max-4*10**(-4)*(10**(G_max/10))*phi**2
        if (phi_m < phi <= phi_r2):
            return 0.75*G_max-7
        if (phi_r2 < phi <= phi_b2):
            return 53-(G_max/2)-25*math.log(phi)
        if (phi_b2 < phi <= 180):
            return 11-G_max/2
    if (10 <= G_max < 22):
        if (0 <= phi <= phi_m):
            return G_max-4*10**(-4)*(10**(G_max/10))*phi**2
        if (phi_m < phi <= phi_r3):
            return 0.75*G_max-7
        if (phi_r3 < phi <= phi_b3):
            return 53-(G_max/2)-25*math.log(phi)
        if (phi_b3 < phi <= 180):
            return 0

class Device():
    ''' Describe a device in an antenna system

        Requires: a name string
        Accepts: floating point values for gain and noise_figure or temperature

        gain defaults to 0.0
    '''

    def __init__(self, name, gain=0.0, temperature=260.0, noise_figure=None):
        self.name = name
        self.gain = gain
        if (temperature == None) and (noise_figure == None):
            error_msg = 'A Noise Figure or Temperature must be supplied.'
            raise Exception(error_msg)
        if noise_figure != None:
            self.noise_figure = noise_figure
            self.temperature = NF_to_T_noise(self.noise_figure)
        else:
            self.temperature = temperature
            self.noise_figure = T_noise_to_NF(self.temperature)

    def __repr__(self):
        return "Device({}, {}, {})".format(self.name, self.temperature,
                                           self.noise_figure)
    
    def __str__(self):
        line1 = '\nDevice:\t{}'.format(self.name)
        line2 = '\n\tGain:\t{}dB'.format(self.gain)
        line3 = '\n\tT:\t{}K'.format(self.temperature)
        line4 = '\n\tNF:\t{}dB'.format(self.noise_figure)
        return (line1 + line2 + line3 + line4)

