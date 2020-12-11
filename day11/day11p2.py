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

def print_seats(seats):
    for s in seats:
        print(''.join(s))
    print()
    print()

def get_seat(seats, pos):
    # print(pos)
    if pos[0] < 0 or pos[0] >= len(seats):
        raise IndexError()
    if pos[1] < 0 or pos[1] >= len(seats[0]):
        raise IndexError()
    return seats[pos[0]][pos[1]]

def get_dseat(seats, pos, direction):
    # print(pos)
    try:
      while True:
        pos = addpos(pos, direction)
        s = get_seat(seats, pos)
        if s != '.':
            return s
    except IndexError:
      return '.'

def alldirs():
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            p = (x, y)
            if p != (0, 0):
                yield p


def process_seats(seats):
    newseats = deepcopy(seats)
    occupied = 0
    for y, row in enumerate(seats):
        for x, s in enumerate(row):
            mypos = (y, x)
            if s == '.':
                continue
            adj = sum(1 if '#' == get_dseat(seats, mypos, p) else 0 for p in alldirs())
            sval = s
            if s == 'L':
                if adj == 0:
                    sval = '#'
            else:
                # print(adj, mypos)
                sval = 'L' if adj >= 5 else '#'
            occupied += 1 if sval == '#' else 0
            newseats[y][x] = sval
    return occupied, newseats



if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "TEST":
        import doctest
        doctest.testmod()
        sys.exit(0)

    logging.basicConfig(level=logging.INFO)
    path = "day11.txt"
    if len(sys.argv) > 1:
        path = sys.argv[1]

    with open(path) as f:
        seats = [list(s.strip()) for s in f.readlines()]

    c = 0
    while True:
        print(c)
        print_seats(seats)        
        
        c2, seats = process_seats(seats)
        if c == c2:
            break
        c = c2
