#!/usr/bin/env python3
from __future__ import print_function

import sys
import os
import math
import pprint
import re
import doctest
import itertools
import collections
import logging
from collections import defaultdict
from functools import reduce

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

from advent import *

class Bag(object):
    def __init__(self, name):
        self.name = name
        self.limits = list() # list of j (cost, element)

    def add_contents(self, quantity, bag):
        self.limits.append((quantity, bag))

    def contains_bag(self, color):
        cnt = sum(c[1] == color for c in self.limits)
        # print("contains " + self.name + " " + color + cnt)
        return cnt > 0

    def __hash__(self):
        return hash(self.name)

    def __equals__(self, x):
        return equals(self.name, x)

    def __repr__(self):
        return self.name +": " + ", ".join( "%d: %s"% (c[0], c[1]) for c in self.limits )

def getbags(color):
    bag = bags[color]
    count = 0
    for bc, bn in bag.limits:
        c = getbags(bn)
        count += c * bc
    return count + 1

def parse_bag(bagrule):
    parts = list(tokenize(bagrule, chars=" ,.\n}"))
    print(parts)
    name = "%s %s" % (parts[0], parts[1])
    yield name
    # print(name)
    i = 4
    while i < len(parts):
        try:
            bcount = int(parts[i])
            bname = "%s %s" % (parts[i+1], parts[i+2])
            yield (bcount, bname)
            i+= 4
        except ValueError:
            break    

contains={}
def find_containing(color):
    for b in bags.values():
        if b.contains_bag(color):
            yield b
        


logging.basicConfig(level=logging.DEBUG)
bags = {}
with open(sys.argv[1]) as f:
    for l in f.readlines():
        b = list(parse_bag(l))
        try:
            bag = bags[b[0]]
        except KeyError:
            bag = Bag(b[0])
        for c in b[1:]:
            bag.add_contents(*c)
        bags[bag.name] = bag

for b in sorted(bags.keys()):
    print(bags[b])

allbags = set(["shiny gold"])
lastlen=0
while len(allbags) > lastlen:
    lastlen = len(allbags)
    for b in list(allbags):
        for b2 in find_containing(b):
            allbags.add(b2.name)

print(getbags("shiny gold") - 1)
