# -*- coding: utf-8 -*-
"""Simple distance, velocity, and angle support for Skyfield.

Copyright © 2013–2018 Brandon Rhodes and available under the MIT license:

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


30MAY23 - Kyle Eberhart - Added support for Frequency units and Power units.
Distance default storage changed to meters.

"""
import numpy as np
from numpy import abs, copysign, isnan
from link_engineering.constants import AU_KM, AU_M, C, DAY_S, tau
from link_engineering.descriptorlib import reify
from link_engineering.functions import _to_array, length_of

_dfmt = '{0}{1:02}deg {2:02}\' {3:02}.{4:0{5}}"'
_dsgn = '{0:+>1}{1:02}deg {2:02}\' {3:02}.{4:0{5}}"'
_hfmt = '{0}{1:02}h {2:02}m {3:02}.{4:0{5}}s'

class UnpackingError(Exception):
    """You cannot iterate directly over a Skyfield measurement object."""

class Unit(object):
    """A measurement that can be expressed in several choices of unit."""

    def __getitem__(self, *args):
        """Tell users to ask for a specific unit before indexing or slicing."""
        cls = self.__class__
        name = cls.__name__
        s = 'to use this {0}, ask for its value in a particular unit:\n\n{1}'
        attrs = sorted(k for k, v in cls.__dict__.items()
                       if k[0].islower() and isinstance(v, (getset, reify)))
        examples = ['    {0}.{1}'.format(name.lower(), attr) for attr in attrs]
        raise UnpackingError(s.format(name, '\n'.join(examples)))

    __iter__ = __getitem__   # give advice about both foo[i] and "x,y,z = foo"

class getset(object):
    """Unit name that serves as both a class constructor and instance attribute.

    This supports two use cases:

    * When called as a class method like ``Distance.km(5.0)``, we build
      and return an instance of ``Distance`` whose ``km`` has been set
      to 5.0 and whose base unit ``m``, using the appropriate conversion
      factor, has been set to 5000.0.

    * When invoked like ``d.km`` on a particular ``Distance`` that
      doesn't yet have a ``km`` attribute (which otherwise Python itself
      would have returned), we apply the conversion factor to ``d.m``
      and return the result.

    """
    def __init__(self, name, docstring, conversion_factor=None, core_unit=None, **kwargs):
        self.name = name
        self.__doc__ = docstring
        self.conversion_factor = conversion_factor
        self.core_unit = core_unit
        self.inverse_function = kwargs.get('inverse', None)

    def __get__(self, instance, objtype=None):
        if instance is None:  # the class itself has been asked for this name
            def constructor(value):
                value = _to_array(value)
                obj = objtype.__new__(objtype)
                setattr(obj, self.name, value)
                conversion_factor = self.conversion_factor
                if conversion_factor is not None:
                    if callable(conversion_factor):
                        setattr(obj, self.core_unit, conversion_factor(value))
                    else:
                        setattr(obj, self.core_unit, value / conversion_factor)
                return obj
            constructor.__doc__ = self.__doc__
            return constructor
        if callable(self.conversion_factor):
            value = self.inverse_function(getattr(instance, self.core_unit))
        else:
            value = getattr(instance, self.core_unit) * self.conversion_factor
        instance.__dict__[self.name] = value
        return value

class Power(Unit):
    """A Power, stored internally as Watts and available in other units.

    You can initialize a ``Power`` by providing a single float or a
    float array as either an ``kW=``, ``W=``, ``mW=``, or ``dB=`` parameter.

    You can access the magnitude of the power with its
    attributes ``.kW``, ``.W``, ``.mW``, and ``.dB``.  By default a power
    prints itself in Watts (W), but you can take control
    of the formatting and choice of units yourself using standard Python
    numeric formatting:

    >>> p = Power(W=.001)
    >>> print(p)
    .001 W
    >>> print('{:.2f} mW'.format(p.mW))
    1.00 mW

    """
    _warned = False

    def __init__(self, kW=None, W=None, mW=None, dBm=None, dBw=None):
        if kW is not None:
            self.kW = _to_array(kW)
            self.W = kW * 1000
        elif W is not None:
            self.W = W = _to_array(W)
        elif mW is not None:
            self.mW = mW = _to_array(mW)
            self.W = mW / 1000
        elif dBw is not None:
            self.dBw = dBw = _to_array(dBw)
            self.W = np.power(10, dBw/10)
        elif dBm is not None:
            self.dBm = dBm = _to_array(dBm)
            self.W = np.power(10, (dBm-30)/10)
        else:
            raise ValueError('to construct a Frequency provide kW, W, mW, or dB')

    kW = getset('kW', 'Kilowatt', 0.001, 'W')
    W = getset('W', 'Watt')
    mW = getset('mW', 'Milliwatt', 1000.0, 'W')
    dBw = getset('dBw', 'deciBel', (lambda a: np.power(10, (a)/10)), 'W', inverse=(lambda a: 10*np.log10(a)))
    dBm = getset('dBm', 'deciBel', (lambda a: np.power(10, (a-30)/10)), 'W', inverse=(lambda a: 10*np.log10(a)+30))

    def __str__(self):
        n = self.W
        return ('{0} W' if getattr(n, 'shape', 0) else '{0:.6} W').format(n)

    def __repr__(self):
        return '<{0} {1}>'.format(type(self).__name__, self)

class Frequency(Unit):
    """A Frequency, stored internally as GHz and available in other units.

    You can initialize a ``Frequency`` by providing a single float or a
    float array as either an ``Hz=``, ``KHz``, ``MHz=``, or ``GHz=`` parameter.

    You can access the magnitude of the Frequency with its
    attributes ``.Hz``, ``KHz``, ``.MHz``, and ``.GHz``.  By default a Frequency
    prints itself in GigaHertz (GHz), but you can take control
    of the formatting and choice of units yourself using standard Python
    numeric formatting:

    >>> f = Frequency(GHz=4)
    >>> print(f)
    4.0 GHz
    >>> print('{:.2f} MHz'.format(f.MHz))
    4000.00 MHz

    """
    _warned = False

    def __init__(self, Hz=None, KHz=None, MHz=None, GHz=None):
        if Hz is not None:
            self.Hz = _to_array(Hz)
            self.GHz = Hz / 1000000000
        elif KHz is not None:
            self.KHz = KHz = _to_array(KHz)
            self.GHz = KHz / 1000000
        elif MHz is not None:
            self.MHz = MHz = _to_array(MHz)
            self.GHz = MHz / 1000
        elif GHz is not None:
            self.GHz = GHz = _to_array(GHz)
        else:
            raise ValueError('to construct a Frequency provide Hz, KHz, MHz, or GHz')
        self.wl = C/self.Hz

    Hz = getset('Hz', 'Hertz', 1000000000, 'GHz')
    KHz = getset('KHz', 'KiloHertz', 1000000, 'GHz')
    MHz = getset('MHz', 'MegaHertz', 1000, 'GHz')
    GHz = getset('GHz', 'GigaHertz')

    def __str__(self):
        n = self.GHz
        return ('{0} GHz' if getattr(n, 'shape', 0) else '{0:.6} GHz').format(n)

    def __repr__(self):
        return '<{0} {1}>'.format(type(self).__name__, self)

class Distance(Unit):
    """A distance, stored internally as m and available in other units.

    You can initialize a ``Distance`` by providing a single float or a float
    array as either an ``au=``, ``km=``, ``m=``, ``cm=``, or ``mm=``  parameter.

    You can access the magnitude of the distance with its attributes ``.au``,
    ``.km``, ``.m``, ``.cm``, and ``.mm``.  By default a distance prints itself in meters (m), but you can take control of the formatting and choice of units yourself using standard Python numeric formatting:

    >>> d = Distance(m=1000)
    >>> print(d)
    1000.0 m
    >>> print('{:.2f} km'.format(d.km))
    1.00 km

    """
    _warned = False

    def __init__(self, au=None, km=None, m=None, cm=None, mm=None):
        if au is not None:
            self.au = _to_array(au)
            self.m = au * AU_M
        elif km is not None:
            self.km = km = _to_array(km)
            self.m = km * 1000
        elif m is not None:
            self.m = m = _to_array(m)
        elif cm is not None:
            self.cm = _to_array(cm)
            self.m = cm / 100
        elif mm is not None:
            self.mm = _to_array(mm)
            self.m = mm / 1000
        else:
            raise ValueError('to construct a Distance provide au, km, or m')

    au = getset('au', 'Astronomical units'
                ' (the Earth-Sun distance of 149,597,870,700 m).', (lambda a: a*AU_M), 'm', inverse=(lambda a: a/AU_M))
    km = getset('km', 'Kilometers (1,000 meters).', .001, 'm')
    m = getset('m', 'Meters.')
    cm = getset('cm', 'Centimeters', 100, 'm')
    mm = getset('mm', 'Millimeters', 1000, 'm')

    def __str__(self):
        n = self.m
        return ('{0} au' if getattr(n, 'shape', 0) else '{0:.6} m').format(n)

    def __repr__(self):
        return '<{0} {1}>'.format(type(self).__name__, self)

    def length(self):
        """Compute the length when this is an |xyz| vector.

        The Euclidean vector length of this vector is returned as a new
        :class:`~skyfield.units.Distance` object.

        >>> from skyfield.api import Distance
        >>> d = Distance(au=[1, 1, 0])
        >>> d.length()
        <Distance 1.41421 au>

        """
        return Distance(au=length_of(self.au))

    def light_seconds(self):
        """Return the length of this vector in light seconds."""
        return self.m / C

#     def to(self, unit):
#         """Convert this distance to the given AstroPy unit."""
#         from astropy.units import au
#         return (self.au * au).to(unit)

class Velocity(Unit):
    """A velocity, stored internally as au/day and available in other units.

    You can initialize a ``Velocity`` by providing a float or float
    array to its ``au_per_d=`` parameter.

    """
    _warned = False

    # TODO: consider reworking this class to return a Rate object.

    def __init__(self, au_per_d=None, km_per_s=None):
        if km_per_s is not None:
            self.km_per_s = km_per_s = _to_array(km_per_s)
            self.au_per_d = km_per_s * DAY_S / AU_KM
        elif au_per_d is not None:
            self.au_per_d = _to_array(au_per_d)
        else:
            raise ValueError('to construct a Velocity provide'
                             ' au_per_d or km_per_s')

    au_per_d = getset('au_per_d', 'Astronomical units per day.')
    km_per_s = getset('km_per_s', 'Kilometers per second.',
                      AU_KM / DAY_S, 'au_per_d')
    m_per_s = getset('m_per_s', 'Meters per second.',
                     AU_M / DAY_S, 'au_per_d')

    def __str__(self):
        n = self.au_per_d
        fmt = '{0} au/day' if getattr(n, 'shape', 0) else '{0:.6} au/day'
        return fmt.format(n)

    def __repr__(self):
        return '<{0} {1}>'.format(type(self).__name__, self)

#     def to(self, unit):
#         """Convert this velocity to the given AstroPy unit."""
#         from astropy.units import au, d
#         return (self.au_per_d * au / d).to(unit)

class AngleRate(object):
    """The rate at which an angle is changing."""

    # TODO: design and implement public constructor.

    @classmethod
    def _from_radians_per_day(cls, radians_per_day):
        ar = cls()
        ar._radians_per_day = radians_per_day
        return ar

    @reify
    def radians(self):
        """:class:`Rate` of change in radians."""
        return Rate._from_per_day(self._radians_per_day)

    @reify
    def degrees(self):
        """:class:`Rate` of change in degrees."""
        return Rate._from_per_day(self._radians_per_day / tau * 360.0)

    @reify
    def arcminutes(self):
        """:class:`Rate` of change in arcminutes."""
        return Rate._from_per_day(self._radians_per_day / tau * 21600.0)

    @reify
    def arcseconds(self):
        """:class:`Rate` of change in arcseconds."""
        return Rate._from_per_day(self._radians_per_day / tau * 1296000.0)

    @reify
    def mas(self):
        """:class:`Rate` of change in milliarcseconds."""
        return Rate._from_per_day(self._radians_per_day / tau * 1.296e9)

    # TODO: str; repr; conversion to AstroPy units

class Rate(object):
    """Measurement whose denominator is time."""

    # TODO: design and implement public constructor.

    @classmethod
    def _from_per_day(cls, per_day):
        r = cls()
        r._per_day = per_day
        return r

    @reify
    def per_day(self):
        """Units per day of Terrestrial Time."""
        return self._per_day

    @reify
    def per_hour(self):
        """Units per hour of Terrestrial Time."""
        return self._per_day / 24.0

    @reify
    def per_minute(self):
        """Units per minute of Terrestrial Time."""
        return self._per_day / 1440.0

    @reify
    def per_second(self):
        """Units per second of Terrestrial Time."""
        return self._per_day / 86400.0

# Angle units.

_instantiation_instructions = """to instantiate an Angle, try one of:

Angle(angle=another_angle)
Angle(radians=value)
Angle(degrees=value)
Angle(hours=value)

where `value` can be either a Python float, a list of Python floats,
or a NumPy array of floats"""

class Angle(Unit):

    def __init__(self, angle=None, radians=None, degrees=None, hours=None,
                 preference=None, signed=False):

        if angle is not None:
            if not isinstance(angle, Angle):
                raise ValueError(_instantiation_instructions)
            self.radians = angle.radians
        elif radians is not None:
            self.radians = _to_array(radians)
        elif degrees is not None:
            self._degrees = degrees = _to_array(_unsexagesimalize(degrees))
            self.radians = degrees / 360.0 * tau
        elif hours is not None:
            self._hours = hours = _to_array(_unsexagesimalize(hours))
            self.radians = hours / 24.0 * tau

        self.preference = (preference if preference is not None
                           else 'hours' if hours is not None
                           else 'degrees')
        self.signed = signed

    @classmethod
    def from_degrees(cls, degrees, signed=False):
        degrees = _to_array(_unsexagesimalize(degrees))
        self = cls.__new__(cls)
        self.degrees = degrees
        self.radians = degrees / 360.0 * tau
        self.preference = 'degrees'
        self.signed = signed
        return self

    radians = getset('radians', 'Radians (𝜏 = 2𝜋 in a circle).')

    @reify
    def _hours(self):
        return self.radians * 24.0 / tau

    @reify
    def _degrees(self):
        return self.radians * 360.0 / tau

    @reify
    def hours(self):
        r"""Hours (24\ |h| in a circle)."""
        if self.preference != 'hours':
            raise WrongUnitError('hours')
        return self._hours

    @reify
    def degrees(self):
        """Degrees (360° in a circle)."""
        if self.preference != 'degrees':
            raise WrongUnitError('degrees')
        return self._degrees

    def arcminutes(self):
        """Return the angle in arcminutes."""
        return self._degrees * 60.0

    def arcseconds(self):
        """Return the angle in arcseconds."""
        return self._degrees * 3600.0

    def mas(self):
        """Return the angle in milliarcseconds."""
        return self._degrees * 3600000.0

    def __str__(self):
        size = self.radians.size
        if size == 0:
            return 'Angle []'
        if self.preference == 'degrees':
            v = self._degrees
            fmt = _dsgn.format if self.signed else _dfmt.format
            places = 1
        else:
            v = self._hours
            fmt = _hfmt.format
            places = 2
        if size >= 2:
            return '{0} values from {1} to {2}'.format(
                len(v), _sfmt(fmt, v[0], places), _sfmt(fmt, v[-1], places))
        return _sfmt(fmt, v, places)

    def __repr__(self):
        if self.radians.size == 0:
            return '<{0} []>'.format(type(self).__name__)
        else:
            return '<{0} {1}>'.format(type(self).__name__, self)

    def hms(self, warn=True):
        """Convert to a tuple (hours, minutes, seconds).

        All three quantities will have the same sign as the angle itself.

        """
        if warn and self.preference != 'hours':
            raise WrongUnitError('hms')
        sign, units, minutes, seconds = _sexagesimalize_to_float(self._hours)
        return sign * units, sign * minutes, sign * seconds

    def signed_hms(self, warn=True):
        """Convert to a tuple (sign, hours, minutes, seconds).

        The ``sign`` will be either +1 or -1, and the other quantities
        will all be positive.

        """
        if warn and self.preference != 'hours':
            raise WrongUnitError('signed_hms')
        return _sexagesimalize_to_float(self._hours)

    def hstr(self, places=2, warn=True, format=_hfmt):
        """Return a string like ``12h 07m 30.00s``; see `Formatting angles`.

        .. versionadded:: 1.39

           Added the ``format=`` parameter.

        """
        if warn and self.preference != 'hours':
            raise WrongUnitError('hstr')
        hours = self._hours
        shape = getattr(hours, 'shape', ())
        fmt = format.format  # `format()` method of `format` string
        if shape:
            return [_sfmt(fmt, h, places) for h in hours]
        return _sfmt(fmt, hours, places)

    def dms(self, warn=True):
        """Convert to a tuple (degrees, minutes, seconds).

        All three quantities will have the same sign as the angle itself.

        """
        if warn and self.preference != 'degrees':
            raise WrongUnitError('dms')
        sign, units, minutes, seconds = _sexagesimalize_to_float(self._degrees)
        return sign * units, sign * minutes, sign * seconds

    def signed_dms(self, warn=True):
        """Convert to a tuple (sign, degrees, minutes, seconds).

        The ``sign`` will be either +1 or -1, and the other quantities
        will all be positive.

        """
        if warn and self.preference != 'degrees':
            raise WrongUnitError('signed_dms')
        return _sexagesimalize_to_float(self._degrees)

    def dstr(self, places=1, warn=True, format=None):
        """Return a string like ``181deg 52' 30.0"``; see `Formatting angles`.

        .. versionadded:: 1.39

           Added the ``format=`` parameter.

        """
        if warn and self.preference != 'degrees':
            raise WrongUnitError('dstr')
        degrees = self._degrees
        signed = self.signed
        if format is None:
            format = _dsgn if signed else _dfmt
        fmt = format.format  # `format()` method of `format` string
        shape = getattr(degrees, 'shape', ())
        if shape:
            return [_sfmt(fmt, d, places) for d in degrees]
        return _sfmt(fmt, degrees, places)

#     def to(self, unit):
#         """Convert this angle to the given AstroPy unit."""
#         from astropy.units import rad
#         return (self.radians * rad).to(unit)
# 
#         # Or should this do:
#         from astropy.coordinates import Angle
#         from astropy.units import rad
#         return Angle(self.radians, rad).to(unit)

class WrongUnitError(ValueError):

    def __init__(self, name):
        unit = 'hours' if (name.startswith('h') or '_h' in name) else 'degrees'
        usual = 'hours' if (unit == 'degrees') else 'degrees'
        message = ('this angle is usually expressed in {0}, not {1};'
                   ' if you want to use {1} anyway,'.format(usual, unit))
        if name == unit:
            message += ' then please use the attribute _{0}'.format(unit)
        else:
            message += ' then call {0}() with warn=False'.format(name)
        self.args = (message,)

def _sexagesimalize_to_float(value):
    """Decompose `value` into units, minutes, and seconds.

    Note that this routine is not appropriate for displaying a value,
    because rounding to the smallest digit of display is necessary
    before showing a value to the user.  Use `_sexagesimalize_to_int()`
    for data being displayed to the user.

    This routine simply decomposes the floating point `value` into a
    sign (+1.0 or -1.0), units, minutes, and seconds, returning the
    result in a four-element tuple.

    >>> _sexagesimalize_to_float(12.05125)
    (1.0, 12.0, 3.0, 4.5)
    >>> _sexagesimalize_to_float(-12.05125)
    (-1.0, 12.0, 3.0, 4.5)

    """
    sign = np.sign(value)
    n = abs(value)
    minutes, seconds = divmod(n * 3600.0, 60.0)
    units, minutes = divmod(minutes, 60.0)
    return sign, units, minutes, seconds

def _sexagesimalize_to_int(value, places=0):
    """Decompose `value` into units, minutes, seconds, and second fractions.

    This routine prepares a value for sexagesimal display, with its
    seconds fraction expressed as an integer with `places` digits.  The
    result is a tuple of five integers:

    ``(sign [either +1 or -1], units, minutes, seconds, second_fractions)``

    The integers are properly rounded per astronomical convention so
    that, for example, given ``places=3`` the result tuple ``(1, 11, 22,
    33, 444)`` means that the input was closer to 11u 22' 33.444" than
    to either 33.443" or 33.445" in its value.

    """
    power = 10 ** places
    n = int((power * 3600 * value + 0.5) // 1.0)
    sign = np.sign(n)
    n, fraction = divmod(abs(n), power)
    n, seconds = divmod(n, 60)
    n, minutes = divmod(n, 60)
    return sign, n, minutes, seconds, fraction

def _sfmt(fmt, value, places):
    """Decompose floating point `value` into sexagesimal, and format."""
    if isnan(value):
        return 'nan'
    sgn, h, m, s, fraction = _sexagesimalize_to_int(value, places)
    sign = '-' if sgn < 0.0 else ''
    return fmt(sign, h, m, s, fraction, places)

def wms(whole, minutes=0.0, seconds=0.0):
    """Return a quantity expressed with 1/60 minutes and 1/3600 seconds."""
    return (whole
            + copysign(minutes, whole) / 60.0
            + copysign(seconds, whole) / 3600.0)

def _unsexagesimalize(value):
    """Return `value` after interpreting a (units, minutes, seconds) tuple.

    When `value` is not a tuple, it is simply returned.

    >>> _unsexagesimalize(3.25)
    3.25

    An input tuple is interpreted as units, minutes, and seconds.  Note
    that only the sign of `units` is significant!  So all of the
    following tuples convert into exactly the same value:

    >>> '%f' % _unsexagesimalize((-1, 2, 3))
    '-1.034167'
    >>> '%f' % _unsexagesimalize((-1, -2, 3))
    '-1.034167'
    >>> '%f' % _unsexagesimalize((-1, -2, -3))
    '-1.034167'

    """
    if isinstance(value, tuple):
        components = iter(value)
        value = next(components)
        factor = 1.0
        for component in components:
            factor *= 60.0
            value += copysign(component, value) / factor
    return value

def _interpret_angle(name, angle_object, angle_float, unit='degrees'):
    """Return an angle in radians from one of two arguments.

    It is common for Skyfield routines to accept both an argument like
    `alt` that takes an Angle object as well as an `alt_degrees` that
    can be given a bare float or a sexagesimal tuple.  A pair of such
    arguments can be passed to this routine for interpretation.

    """
    if angle_object is not None:
        if isinstance(angle_object, Angle):
            return angle_object.radians
    elif angle_float is not None:
        return _unsexagesimalize(angle_float) / 360.0 * tau
    raise ValueError('you must either provide the {0}= parameter with'
                     ' an Angle argument or supply the {0}_{1}= parameter'
                     ' with a numeric argument'.format(name, unit))

def _ltude(value, name, psuffix, nsuffix):
    # Support for old deprecated Topos argument interpretation.
    if not isinstance(value, str):
        return _unsexagesimalize(value)
    value = value.strip().upper()
    if value.endswith(psuffix):
        sign = +1.0
    elif value.endswith(nsuffix):
        sign = -1.0
    else:
        raise ValueError('your {0} string {1!r} does not end with either {2!r}'
                         ' or {3!r}'.format(name, value, psuffix, nsuffix))
    try:
        value = float(value[:-1])
    except ValueError:
        raise ValueError('your {0} string {1!r} cannot be parsed as a floating'
                         ' point number'.format(name, value))
    return sign * value
