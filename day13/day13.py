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

# [200~The time this loop takes a particular bus is also its ID number: the bus with ID 5 departs from the sea port at timestamps 0, 5, 10, 15, and so on. The bus with ID 11 departs at 0, 11, 22, 33, and so on. If you are there when the bus departs, you can ride that bus to the airport!
    pprint(data)

    t = int(data[0])
    buses = {}
    for n, b in enumerate(data[1].split(',')):
        if b != 'x':
            buses[n] = int(b)

    
    m = [ (b - (t % b), b) for b in buses.values()]
    print(m)
    print(min(m))
    mn = min(m)
    print(mn[0] * mn[1])

