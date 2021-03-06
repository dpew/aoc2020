#!/usr/bin/env python3

import sys
import math
import pprint
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
from intcode import *

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "TEST":
        import doctest
        doctest.testmod()
        sys.exit(0)

    logging.basicConfig(level=logging.INFO)
    path = "day12.txt"
    if len(sys.argv) > 1:
        path = sys.argv[1]

    with open(path) as f:
        paths = f.readlines()


    dist = 0
    heading = (0, 1)
    pos = (0, 0)
    for p in paths:
        m = p[0]
        d = int(p[1:])
        if m == 'F':
            v = mulpos(d, heading)
        elif m == 'N':
            v = (d, 0)
        elif m == 'S':
            v = (-d, 0)
        elif m == 'E':
            v = (0, d)
        elif m == 'W':
            v = (0, -d)
        elif m == 'R':
            heading = rotate2(heading, d)
            continue
        elif m == 'L':
            heading = rotate2(heading, -d)
            continue
        else:
            raise ValueError(p)
        pos = addpos(v, pos)
        print(pos)
    print(mdistance((0, 0), pos))
