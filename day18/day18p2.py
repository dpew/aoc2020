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

def toPostfix(infix):
    stack = []
    postfix = ''

    for c in infix:
        if c in '+*':
            postfix += c
        else:
            if c == '(':
                stack.append(c)
            elif stack and c == ')':
                operator = stack.pop()
                while stack and not operator == '(':
                    postfix += operator
                    operator = stack.pop()
            else:
                while stack: # and hasLessOrEqualPriority(c,stack[-1]):
                    postfix += stack.pop()
                stack.append(c)

    while stack:
        postfix += stack.pop()
    return postfix

def infixToPostfix(infixexpr):
    prec = {}
    prec["*"] = 2
    prec["/"] = 2
    prec["+"] = 3
    prec["-"] = 3
    prec["("] = 1
    opStack = deque()
    postfixList = []
    tokenList = infixexpr #infixexpr.split()

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
            postfixList.append(token)
        elif token == '(':
            opStack.append(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while opStack and prec[opStack[-1]] >= prec[token]:
                  postfixList.append(opStack.pop())
            opStack.append(token)

    while opStack:
        postfixList.append(opStack.pop())
    return postfixList

        
def evaluate(vals):
    '''
        >>> evaluate(splitline('(6) + 8'))
        14
        >>> evaluate(splitline('(1 + 5 * ( 6 ) + 8)'))
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
    postfix = deque(infixToPostfix(vals))
    #print(''.join(vals), postfix)
    q = deque()
    for v in postfix:
        if v in OPERS:
            r = OPERS[v](q.pop(), q.pop())
            q.append(r)
        else:
            q.append(int(v))
    return q[0]

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
