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
# import networkx as nx
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

class Computer(object):

    def __init__(self, memory):
        self.acc = 0
        self.pc = 0
        self.memory = memory
        self.seen = set()

    def step(self):
        if self.pc in self.seen:
            raise ValueError("seen")
        self.seen.add(self.pc)
        inst = self.memory[self.pc]
        if inst[0] == 'nop':
            self.pc += 1
        elif inst[0] == 'jmp':
            self.pc += inst[1]
        elif inst[0] == 'acc':
            self.pc += 1
            self.acc += inst[1]
        else:
            raise IndexError("bad instruction")

def parseline(line):
    l = list(tokenize(line, " "))
    return (l[0], int(l[1]))

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "TEST":
        import doctest
        doctest.testmod()
        sys.exit(0)

    logging.basicConfig(level=logging.INFO)
    path = "day8.txt"
    if len(sys.argv) > 1:
        path = sys.argv[1]

    with open(path) as f:
        memory = [ parseline(x) for x in f.readlines()]

    c = Computer(memory)
    while True:
        try:
            c.step()
        except:
            break

    print(c.acc)