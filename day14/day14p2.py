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

def applyMask(mask, addr, maskV, maskX, maskShift, addressInc):
    print('-----')
    incShift = 0
    print('M ', mask)
    print('MX', mask2str(maskX))
    print("MV", mask2str(maskV))
    for b, s in enumerate(maskShift):
        if s >= 0:
            bmask = 1 << b
            bit = 1 if addressInc & bmask else 0
#            print('BIT', b, bit, mask2str(bmask))
            vmask = bit << s
            incShift |= vmask
#    print(maskShift)
    print('V1', mask2str(addr), addr, addressInc)
    print('M ', mask)
    v = ~maskX & addr
    print('-')
    print('V2', mask2str(v))
    print("MV", mask2str(maskV))
    v = v | maskV
    print('-')
    print("V3", mask2str(v))
    print('IN', mask2str(incShift), addressInc)
    v = v | incShift
    print("V4", mask2str(v), addr, v)
    return v

class Masks:

    def __init__(self, mask):
        self.mask = mask


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
    for inst in data:
        cmd = inst[0]
        print("INST", inst)
        if cmd == 'mask':
            print('='*40)
            mask = inst[1]
            maskV = int(inst[1].replace('X','0'), 2)
            maskX = int(inst[1].replace('1', '0').replace('X', '1'), 2)
            maskC = sum(1 if x == 'X' else 0 for x in inst[1])
            # maskShift = [ 35 - e[0] if e[1] == 'X' else -1 for e in enumerate(inst[1]) ]
            maskShift = [ 35 - e[0] for e in enumerate(inst[1]) if e[1] == 'X']
            #print('MV', mask2str(maskV))
            #print('MX', mask2str(maskX))
            #print(mask2str(5))
        elif cmd == 'mem':
            mr = int(inst[1])
            nv = int(inst[2])
            for inc in range(2 ** maskC):
                mr2 = applyMask(mask, mr, maskV, maskX, maskShift, inc)
                print("MEMORY[%d]=%d" % (mr2, nv))
                memory[mr2] = nv
        else:
            raise False
    print(sum(memory.values()))
