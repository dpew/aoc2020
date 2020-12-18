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

def neighbors(pos):
    for x in range(-1, 2):
       for y in range(-1, 2):
          for z in range(-1, 2):
              p = (x, y, z)
              if p != (0, 0, 0):
                 yield addpos(pos, p)

class Cube(object):

    def __init__(self):
        self.cubes = defaultdict(lambda: '.')
        self.min = (0, 0, 0)
        self.max = (0, 0, 0)

    def get(self, pos):
        return self.cubes[pos]

    def set(self, pos, val):
        v = self.cubes[pos]
        self.cubes[pos] = val
        if val == '#':
           self.min = mintuple(self.min, pos)
           self.max = maxtuple(self.max, pos)
        return v

    def getslice(self, s):
        rows = []
        for x in range(self.min[0], self.max[0]+1):
           rows.append(''.join(self.get((x, y, s)) for y in range(self.min[1], self.max[1]+1)))
        return '\n'.join(rows)

    def count_neighbors(self, pos):
        cnt = sum(1 if self.get(p) == '#' else 0 for p in neighbors(pos))
        return cnt

    def cycle(self):
        newcube = Cube()
        for x in range(self.min[0]-1, self.max[0]+2):
          for y in range(self.min[1]-1, self.max[1]+2):
            for z in range(self.min[2]-1, self.max[2]+2):
                p = (x, y, z)
                cv = self.get(p)
                nv = '.'
                if cv == '.' and self.count_neighbors(p) == 3:
                    nv = '#'
                if cv == '#' and self.count_neighbors(p) in (2, 3):
                    nv = '#'
                newcube.set(p, nv)

        return newcube


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
        slices = [ s.strip() for s in f.readlines()]

    cube = Cube()
    for x, row in enumerate(slices):
        for y, v in enumerate(row):
            cube.set((x, y, 0), v)

    print(cube.cubes)
    print(cube.min, cube.max)
    print(cube.getslice(0))
    for c in range(6):
        cube = cube.cycle()
        print(cube.getslice(0))

    print(sum(1 if c == '#' else 0 for c in cube.cubes.values()))
