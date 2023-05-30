"""Various constants required by Skyfield.

Copyright © 2013–2018 Brandon Rhodes and available under the MIT license:

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# Definitions.
AU_M = 149597870700             # per IAU 2012 Resolution B2
AU_KM = 149597870.700
ASEC360 = 1296000.0
DAY_S = 86400.0

# Angles.
ASEC2RAD = 4.848136811095359935899141e-6
DEG2RAD = 0.017453292519943296
RAD2DEG = 57.295779513082321
pi = 3.141592653589793
tau = 6.283185307179586476925287  # lower case, for symmetry with math.pi

# Physics.
C = 299792458.0                            # m/s
GM_SUN_Pitjeva_2005_km3_s2 = 132712440042  # Elena Pitjeva, 2015JPCRD..44c1210P

# Earth and its orbit.
ANGVEL = 7.2921150e-5           # radians/s
ERAD = 6378136.6                # meters
IERS_2010_INVERSE_EARTH_FLATTENING = 298.25642

# Heliocentric gravitational constant in meters^3 / second^2, from DE-405.
GS = 1.32712440017987e+20

# Time.
T0 = 2451545.0
B1950 = 2433282.4235

C_AUDAY = C * DAY_S / AU_M
