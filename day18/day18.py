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

OPERS = {
   '+': lambda a, b: a + b,
   '*': lambda a, b: a * b
}

config = {
        r'd': 'number',
        r'\+': 'plus',
        r'\*': 'mul',
        r'\(': 'lp',
        r'\)': 'rp' }

def splitline(line):
    '''
       >>> splitline('1 + 4 + (5 * 6)')
       deque(['1', '+', '4', '+', '(', '5', '*', '6', ')'])
    '''
    return deque(filter(lambda x: x != ' ', line.strip()))

def evaluate(vals):
    '''
        >>> evaluate(splitline('(6) + 8'))
        14
        >>> evaluate(splitline('1 + 5 * ( 6 ) + 8)'))
        44
        >>> evaluate(splitline('(1+5*(6)+8)'))
        44
        >>> evaluate(splitline('(1+5*(6+4)+8)'))
        68
        >>> evaluate(splitline('(1+5*((6)+4)+8)'))
        68
        >>> evaluate(splitline('(1+5*((6)+4)+8)'))
        68
    '''
    #print('eval(', ''.join(vals))
    right = vals.pop()
    if right == ')':
        right = evaluate(vals)
    else:
        right = int(right)
    if len(vals) == 0:
        return right
    oper = vals.pop()
    if oper == '(':
        return right
    ofunc = OPERS[oper]
    left = evaluate(vals)
    #print(left, oper, right)
    result = ofunc(left, right)
    #if len(vals) > 0 and vals[-1] == '(':
    #    vals.pop()
    return result

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
        data = f.readlines()

    s = 0
    for eq in data:
        r = evaluate(splitline(eq))
        print(r, eq)
        s += r

    print(s)
