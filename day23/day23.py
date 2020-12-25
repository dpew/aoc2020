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

if __name__ == '__main__':
  if len(sys.argv) == 2 and sys.argv[1] == "TEST":
    import doctest
    doctest.testmod()
    sys.exit(0)

  logging.basicConfig(level=logging.INFO)
  puzzle = "362981754"
  steps = 100
  if len(sys.argv) > 1:
    puzzle = sys.argv[1]
  if len(sys.argv) > 2:
    steps = int(sys.argv[2])

  def lookfor(label, pickup, cups):
      dest = label - 1
      while True:
          if dest == 0:
             dest = 9
          if dest not in pickup:
              break
          dest = dest - 1
      return dest, cups.index(dest)

  cups = deque(int(c) for c in puzzle) 
  for move in range(steps):
     qstr = repr(cups)
     label = cups[0]
     cups.rotate(-1)
     pickup = [ cups.popleft() for x in range(3) ]
     dest, destidx = lookfor(label, pickup, cups)
     print('-- move %d --\ncups: %s\nlabel: %d\npick up: %s\ndest: %d' % (move+1, qstr, label, pickup, dest))
     for c in reversed(pickup):
         cups.insert(destidx+1, c)

  print(cups)
