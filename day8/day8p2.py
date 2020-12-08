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

    def __init__(self, memory, jswap=0, nswap=0):
        self.acc = 0
        self.pc = 0
        self.memory = list(memory)
        self.seen = set()
        self.memory[jswap] = ('nop', self.memory[jswap][1])
        # self.memory[nswap] = ('jmp', self.memory[nswap][1])
        # n = self.memory[nswap]
        # self.memory[jswap] = n
        # self.memory[nswap] = j

    def step(self):
        if self.pc > len(memory):
            return -1
        if self.pc == len(memory):
            return 0
        if self.pc in self.seen:
            return -1
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
        return 1

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

    jlist = filter(lambda x: x >= 0,
                   (x[0] if x[1][0] == 'jmp' else -1 for x in enumerate(memory)))
    nlist = filter(lambda x: x >= 0,
                   (x[0] if x[1][0] == 'nop' else -1 for x in enumerate(memory)))
    for j in jlist:
        # for n in nlist:
            c = Computer(memory, j)
            while c.step() > 0:
                pass
            if c.step() == 0:
                print(c.acc, j)
                sys.exit(0)

    print("FAILED TO TERMINATE")
    print(c.acc)
