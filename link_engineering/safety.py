#!/usr/bin/env pyhton3
#
#   Calculate transmit RF safety compliance for parabolic reflectors
#
#   26MAR22 - Kyle Eberhart
#
#------------------------------------------------------------------------------

import link_eng as eng
import math

class Safety():
    ''' Calculate transmit RF safety compliance for parabolic reflectors.

        diam = antenna diameter in meters
        eta = antenna efficiency
        freq = transmit frequency in MHz
        power = HPA power in Watts

        Ref: OET Bulletin 65, Evaluating Compliance with FCC Guidelines for
            Human Exposure to Radiofrequency Electrmagnetic Fields, 1997
    '''
    def __init__(self, diam, freq, power, eta=0.53):
        ''' Calculate transmit RF safety compliance for parabolic reflectors.

            diam = antenna diameter in meters
            freq = transmit frequency in MHz
            power = HPA power in Watts
            eta = antenna efficiency percentage
            limit = the actionable limit of exposure

        '''
        self.diam = diam
        self.eta = eta
        self.freq = freq
        self.power = power

        self.wavelength = eng.calc_wavelength(self.freq*1000000)
        self.gain = eng.calc_ant_G(self.eta, self.diam, self.wavelength)
        self.EIRP = eng.calc_EIRP(self.gain, self.power)
        self.S_surface = eng.S_surface(self.power, self.diam)
        self.R_nf = eng.R_nf(self.diam, self.wavelength)
        self.S_nf = eng.S_nf(self.eta, self.power, self.diam)
        self.R_ff = eng.R_ff(self.diam, self.wavelength)
        self.S_ff = eng.S(self.EIRP, self.R_ff)
        self.R_gnd = (self.diam/2)+1

        # trying to implement near field density estimation
        modded_gain = self.gain - 10.0
        self.S_gnd = self.S_nf/100

        self.S_nf_mW = self.S_nf/10.0
        self.S_ff_mW = self.S_ff/10.0
        self.S_gnd_mW = self.S_gnd/10.0

        self.find_limits()
        self.test_limits()

    def test_limits(self):
        ''' Create and format warning messages based on exposure limits.
        '''
        self.mpe_limit_banner = "Occupational limts:\t{} V/m\t{} A/m\t{} mW/cm^2\t6 minutes\n".format(
                self.mpe_E_limit, self.mpe_H_limit, self.mpe_S_limit)
        self.gp_limit_banner = "General Population:\t{} V/m\t{} A/m\t{} mW/cm^2\t30 minutes\n".format(
                self.gp_E_limit, self.gp_H_limit, self.gp_S_limit)

        nf_mpe_limit = "below MPE"
        if self.S_nf_mW > self.mpe_S_limit:
            nf_mpe_limit = "EXCEEDS MPE"
        nf_gp_limit = "below GP"
        if self.S_nf_mW > self.gp_S_limit:
            nf_gp_limit = "EXCEEDS GP"

        ff_mpe_limit = "below MPE"
        if self.S_ff_mW > self.mpe_S_limit:
            ff_mpe_limit = "EXCEEDS MPE"
        ff_gp_limit = "below GP"
        if self.S_ff_mW > self.gp_S_limit:
            ff_gp_limit = "EXCEEDS GP"

        gnd_mpe_limit = "below MPE"
        if self.S_gnd_mW > self.mpe_S_limit:
            gnd_mpe_limit = "EXCEEDS MPE"
        gnd_gp_limit = "below GP"
        if self.S_gnd_mW > self.gp_S_limit:
            gnd_gp_limit = "EXCEEDS GP"

        self.nf_limit = " & ".join([nf_mpe_limit, nf_gp_limit])
        self.ff_limit = " & ".join([ff_mpe_limit, ff_gp_limit])
        self.gnd_limit = " & ".join([gnd_mpe_limit, gnd_gp_limit])

    def __str__(self):
        line1 = "\nGiven:\t{} m\t{} MHz\t{} W\n".format(self.diam,
                self.freq, self.power)
        line2 = "\n Surface Pwr\t{:.2f} mW/cm^2\t".format((self.S_surface/10.0))
        line3 = "\n On-Axis -"
        line4 = "\n\tNear Field Max Pwr\t{:.2f} mW/cm^2\t{}".format((self.S_nf_mW), self.nf_limit)
        line5 = "\n\tNear Field Extent\t{:.2f} m\t".format(self.R_nf)
        line6 = "\n\tFar Field Onset\t\t{:.2f} m\t".format(self.R_ff)
        line7 = "\n\tFar Field Max Pwr\t{:.2f} mW/cm^2\t{}".format((self.S_ff_mW), self.ff_limit)
        line8 = "\n\n Off-Axis -"
        line9 = "\n   Near Field -"
        line10 = "\n\t{:.1f} m from dish edge\t{:.2f} mW/cm^2\t{}".format(self.diam,
                self.S_gnd_mW, self.gnd_limit)
        end = "\n"

        return (line1 + self.mpe_limit_banner + self.gp_limit_banner +
                line2 + line3 + line4 + line5 +  line6 + line7 + line8 +
                line9 + line10 + end)

    def __repr__(self):
        return "Safety({}, {}, {}, {}, {})".format(self.diam, self.freq,
                self.power, self.eta, self.limit)


    def find_limits(self):
        ''' Determine the Occupational/Controlled and
            General population/uncontrolled limits depending upon frequency.

            freq is frequency in MHz
        '''
        freq = self.freq

        mpe_S_limit = 100.0
        mpe_E_limit = 614.0
        mpe_H_limit = 1.63

        gp_S_limit = 100.0
        gp_E_limit = 614.0
        gp_H_limit = 1.63

        if (freq > 0.3) and (freq < 30.0):
            if freq >= 1.34:
                gp_S_limit = 180.0/math.pow(freq, 2)
                gp_E_limit = 824.0/freq
                gp_H_limit = 2.19/freq
            if freq >= 3.0:
                mpe_S_limit = 900.0/math.pow(freq, 2)
                mpe_E_limit = 1842.0/freq
                mpe_H_limit = 4.89/freq
        if (freq >= 30.0) and (freq < 300.0):
            mpe_S_limit = 1.0
            mpe_E_limit = 61.4
            mpe_H_limit = 0.163
            gp_S_limit = 0.2
            gp_E_limit = 27.5
            gp_H_limit = 0.073
        if (freq >= 300.0) and (freq < 1500.0):
            mpe_S_limit = freq/300.0
            mpe_E_limit = "--"
            mpe_H_limit = "--"
            gp_S_limit = freq/1500.0
            gp_E_limit = "--"
            gp_H_limit = "--"
        if (freq >= 1500.0) and (freq < 100000):
            mpe_S_limit = 5.0
            mpe_E_limit = "--"
            mpe_H_limit = "--"
            gp_S_limit = 1.0
            gp_E_limit = "--"
            gp_H_limit = "--"

        self.mpe_S_limit = mpe_S_limit
        self.mpe_E_limit = mpe_E_limit
        self.mpe_H_limit = mpe_H_limit
        self.gp_S_limit = gp_S_limit
        self.gp_E_limit = gp_E_limit
        self.gp_H_limit = gp_H_limit


if __name__ == "__main__":
    testing = Safety(13, 1791.748, 300)
    print(testing)
