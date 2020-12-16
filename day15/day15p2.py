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

def day15(n, sequence):
    '''
        >>> day15(10, [0, 3, 6])
        0
        >>> day15(2020, [1, 3, 2])
        1
        >>> day15(2020, [2, 1, 3])
        10
        >>> day15(2020, [1, 2, 3])
        27
        >>> day15(2020, [2, 3, 1])
        78
        >>> day15(2020, [3, 2, 1])
        438
        >>> day15(2020, [3, 1, 2])
        1836
    '''
    lastspoken={}

    def getlast(value, index):
        if value in lastspoken:
            v = index - lastspoken[value] 
        else:
            v = 0
        return v

    recent = None
    for turn, v in enumerate(sequence):
        lastspoken[recent] = turn
        recent = v

    for i in range(len(sequence), n):
        v = getlast(recent, i)
        lastspoken[recent] = i
        #print("turn=%d, recent=%d, value=%d" %(i+1, recent, v))
        recent = v
    return recent


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "TEST":
        import doctest
        doctest.testmod()
        sys.exit(0)

    logging.basicConfig(level=logging.INFO)
    path = "input.txt"
    if len(sys.argv) > 1:
        path = sys.argv[1]

    print(day15(30000000, [16,12,1,0,15,7,11]))


