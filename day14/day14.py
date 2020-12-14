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

def mask2str(m):
    return ("0"*36 + bin(m).replace("0b", ""))[-36:]

def applyMask(val, maskV, maskX):
    print('MX', mask2str(maskX))
    print('V1', mask2str(val), val)
    v = maskX & val
    print('V2', mask2str(v))
    print()
    print("MV", mask2str(maskV))
    print('V2', mask2str(v))
    v = maskV | v
    print("V3", mask2str(v), v)
    print('-----')
    return v

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
        data = [ list(tokenize(d, ' =\n[]')) for d in f.readlines()]


    memory = defaultdict(lambda: 0)
    maskV = 0
    maskX = 0
    for inst in data:
        cmd = inst[0]
        if cmd == 'mask':
            print('MM', inst[1])
            maskV = int(inst[1].replace('X','0'), 2)
            maskX = int(inst[1].replace('1', '0').replace('X', '1'), 2)
            print('MV', mask2str(maskV))
            print('MX', mask2str(maskX))
            print(mask2str(5))
        elif cmd == 'mem':
            mr = int(inst[1])
            nv = int(inst[2])
            memory[mr] = applyMask(nv, maskV, maskX)
    print(sum(memory.values()))
