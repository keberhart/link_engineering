#!/usr/bin/env python3
#
#   systems.py - RF systems are described here. uses the link_engineering
#   library.
#
#   Created - 29MAY23 - Kyle Eberhart
#
#------------------------------------------------------------------------------

import link_engineering


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

