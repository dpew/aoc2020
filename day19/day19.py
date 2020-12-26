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

RULES = {}

class ConstRule(object):
    def __init__(self, value):
        self.value = value

    def size(self):
        return len(self.value)

    def match(self, pattern):
        return pattern and pattern.startswith(self.value)

class AndRule(object):
    def __init__(self, rules):
        self.rules = rules

    def size(self):
        return sum(r.size() for r in self.rules)

    def match(self, pattern):
        offset = 0
        for r in self.rules:
            if offset >= len(pattern):
                return False, offset
            if not r.match(pattern[offset:]):
                return False
            offset += r.size()
        return True

class OrRule(object):
    def __init__(self, rules):
        self.rules = rules

    def size(self):
        return self.rules[0].size()

    def match(self, pattern):
        for r in self.rules:
           if r.match(pattern):
               return True
        return False

class RefRule(object):
    def __init__(self, name):
        self.name = name

    def size(self):
        return RULES[self.name].size()

    def match(self, pattern):
        return RULES[self.name].match(pattern)

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
        lines = [r.strip() for r in f.readlines()]

    for row in lines:
        if not row:
            break
        rline = tuple(tokenize(row, ":|"))
        name = rline[0]
        if '"' in rline[1]:
            RULES[name] = ConstRule(tuple(tokenize(rline[1], '" '))[0])
            continue
        orRules = []
        for andRuleStr in rline[1:]:
            refs = tokenize(andRuleStr, " ")
            andRule = AndRule([RefRule(x) for x in refs]) 
            orRules.append(andRule)
        RULES[name] = OrRule(orRules)

    rule0 = RULES["0"]
    rzsize = rule0.size()
    match = []
    for row in lines:
        if not row:
            continue
        elif row[0] in '0123456789':
            continue
        elif len(row) != rzsize:
            print("BADSIZE ", row)
        elif not rule0.match(row):
            print("BADMATCH", row)
        else:
            match.append(row)
    print(len(match), match)
