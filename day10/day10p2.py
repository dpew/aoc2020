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
import numpy as np
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

counts = {}
def permutations(data):
    try:
        return counts[data[0]]
    except KeyError:
        pass
    if len(data) == 2:
        counts[data[0]] = 1
        print(1, data)
        return 1
    if len(data) == 1:
        return 0
    # count the number of adjacent that are 3 or less
    n = data[0]    
    cnt = 0
    for x in range(1, 5):
        if x < len(data) and (data[x] - n) <= 3:
            print(data[x] - n)
            cnt += permutations(data[x:])
        else:
            break
    counts[n] = cnt
    print(cnt, data)
    return cnt

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "TEST":
        import doctest
        doctest.testmod()
        sys.exit(0)

    logging.basicConfig(level=logging.INFO)
    path = "day10.txt"
    if len(sys.argv) > 1:
        path = sys.argv[1]

    with open(path) as f:
        data = [ int(x) for x in f.readlines()]

    data = sorted(data)
    data.insert(0, 0)
    data.append(data[-1] + 3)
    cnt = permutations(tuple(data))
    print(cnt)

