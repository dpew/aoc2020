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

def isvalid(buffer, v):
    # print("Checking ", v, buffer)
    for x, y in itertools.permutations(buffer, 2):
        #print(x, y)
        if x == y:
            continue
        if x + y == v:
            # print("Found ", x, y)
            return True
    return False


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "TEST":
        import doctest
        doctest.testmod()
        sys.exit(0)

    logging.basicConfig(level=logging.INFO)
    path = "day9.txt"
    size = 25
    if len(sys.argv) > 1:
        path = sys.argv[1]
    if len(sys.argv) > 2:
        size = int(sys.argv[2])

    with open(path) as f:
        inputs = list(int(x) for x in f.readlines())

    data = deque(inputs)
    buffer = deque()
    while len(buffer) < size:
        buffer.append(data.popleft())

    invalid = None
    while len(data):
        v = data.popleft()
        if not isvalid(buffer, v):
            print("Not valid!", v)
            invalid = v
        buffer.append(v)
        buffer.popleft()
    
    # Now search for the sum of values that add to invalid
    for l in range(2, len(inputs)):
        data = deque(inputs)
        sumb = deque()
        for a in range(l):
            sumb.append(data.popleft())
        
        while len(data) > 0:
            sumb.popleft()
            sumb.append(data.popleft())
            if invalid == sum(sumb):
                print("Found", min(sumb), max(sumb))
                print(min(sumb) + max(sumb))
                sys.exit(0)
