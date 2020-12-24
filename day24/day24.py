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

import sys
from math import radians, cos, sin, sqrt, ceil, floor

C = cos(radians(30))
print("C", C)

MAPVAL = {
    'e':  (  1,  0),
    'w':  ( -1,  0),
    'ne': ( .5,  C),
    'nw': (-.5,  C),
    'se': ( .5, -C),
    'sw': (-.5, -C)
}

def move(moves):
  '''
     Returns the number of moves it takes to return to start
     >>> move('nwwswee')
     (0.0, 0.0)
  '''
  position = (0, 0)
  while moves:
    move = None
    for k, v in MAPVAL.items():
      if moves.startswith(k):
        move = v
        movestr = k
        moves = moves[len(k):]
        break
    if move is None:
      raise ValueError("Unknown position " + moves)
    position = (round(position[0] + move[0], 4), round(position[1] +  move[1],4))
    #print(movestr, position)
  return position


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
    data = [ d.strip() for d in f.readlines()]

  been = defaultdict(lambda: 0)
  for row in data:
      been[move(row)] += 1

  flipped = sum(1 if x % 2 else 0 for x in been.values())
  flipped2 = sum(1 if x % 2 == 0 else 0 for x in been.values())
  pprint.pprint(dict(been))
  print(flipped, flipped2)
