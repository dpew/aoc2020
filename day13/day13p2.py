#!/usr/bin/env python3

import sys
import math
from pprint import pprint
import os
import re
import doctest
import itertools
import types
import logging
from collections import deque
from collections import defaultdict
#import networkx as nx
from copy import deepcopy
try:
   import matplotlib.pyplot as plt
except ImportError:
   plt = None

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

from advent import *

# From https://math.stackexchange.com/questions/2218763/how-to-find-lcm-of-two-numbers-when-one-starts-with-an-offset


def combine_phased_rotations(a_period, a_phase, b_period, b_phase):
    """Combine two phased rotations into a single phased rotation

    Returns: combined_period, combined_phase

    The combined rotation is at its reference point if and only if both a and b
    are at their reference points.
    """
    print("INPUTS", a_period, a_phase, b_period, b_phase)
    gcd, s, t = extended_gcd(a_period, b_period)
    print("GCD RESULT", gcd, s, t)
    phase_difference = a_phase - b_phase
    print("PD", phase_difference)
    pd_mult, pd_remainder = divmod(phase_difference, gcd)
    print("M, R", pd_mult, pd_remainder)
    if pd_remainder:
        raise ValueError("Rotation reference points never synchronize.")

    combined_period = a_period // gcd * b_period
    print("COMBINED_PERIOD", combined_period)
    combined_phase = (a_phase - s * pd_mult * a_period) % combined_period
    print("COMBINED_PHASE", combined_phase)
    return combined_period, combined_phase

def extended_gcd(a, b):
    """Extended Greatest Common Divisor Algorithm

    Returns:
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def sum_phase(phaseoffsets):
    period1 = phaseoffsets[0][0]
    offset = phaseoffsets[0][1]
    maxoffset = offset
    phase1 = -offset % period1
    for period2, offset2 in phaseoffsets[1:]:
        phase2 = -offset2 % period2
        maxoffset = max(maxoffset, offset2)
        period1, phase1 = combine_phased_rotations(period1, phase1, period2, phase2)
        print(period1, phase1, maxoffset, phase1 + maxoffset)
    print("ANSWER WAS PHASE, not phase1 + maxoffset, not sure why", phase1)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "TEST":
        import doctest
        doctest.testmod()
        sys.exit(0)

    logging.basicConfig(level=logging.INFO)
    path = "input.txt"
    if len(sys.argv) > 1:
        path = sys.argv[1]

    with open(path) as f:
        data = [ x.strip() for x in f.readlines()]

    pprint(data)

    t = int(data[0])
    buses = [(int(b), o) for o, b in enumerate(data[1].split(',')) if b != 'x']
    print(buses)
    sum_phase(buses)
    #for n, b in enumerate(data[1].split(',')):
    #    if b != 'x':
    #        buses[n] = int(b)
