from random import *
from math import *
from time import *

from matplotlib.pyplot import *
from numpy import *
from numpy.fft import *

def gaussian_kernel(rows, columns, spread):
    # Intialize
    g = zeros((rows, columns));
    # Calculate approximate centre
    r_centre = ceil((rows - 1) / 2)
    c_centre = ceil((columns - 1) / 2)
    # Pre-calculate
    a = 1 / (2 * pow(spread, 2))
    # Iterate matrix
    for r in range(rows):
        for c in range(columns):
            # Shift Gaussian to centre
            r_shift = (r - r_centre)
            c_shift = (c - c_centre)
            g[r, c] = exp(-a * (pow(r_shift, 2) + pow(c_shift, 2)))
    # Scale matrix
    g /= pow((spread * sqrt(2 * pi)), 2)
    # Done
    return g

def apply_kernel(rows, columns, f_signal, f_kernel):
    # 1. Shift the signal into position,
    # 2. Apply a kernel in the frequency domain,
    # 3. Then return to spatial domain
    g = ifftn(fftn(ifftshift(f_signal)) * fftn(f_kernel))
    # Remove the complex component
    g = real(g)
    # Done
    return g


