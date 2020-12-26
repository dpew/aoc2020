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
from collections import defaultdict

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

from advent import *

GRAMMAR = {}

def splitand(ors):
    return tuple(int(x) for x in tokenize(ors, " "))

def splitrule(rule):
    return tuple(splitand(a) for a in rule.split("|"))


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
        rline = tuple(tokenize(row, ":"))
        name = int(rline[0])
        if '"' in rline[1]:
            GRAMMAR[name] = list(tokenize(rline[1], '" '))[0]
            continue
        else:
            GRAMMAR[name] = splitrule(rline[1])

    GRAMMAR[8] = ((42,), (42, 8))
    GRAMMAR[11] = ((42,31), (42, 11, 31))
    #pprint.pprint(GRAMMAR)

    def expand_and(r):
        parts = [expand(x) for x in r]
        return [''.join(x) for x in itertools.product(*parts)]

    def expand_or(r):
        for x in r:
            for v in expand_and(x):
                yield v

    def expand(r):
        if isinstance(GRAMMAR[r], str):
            return [GRAMMAR[r]]
        else:
            return list(expand_or(GRAMMAR[r]))

    values42 = expand(42)
    values31 = expand(31)
    print("42: %s\n", pprint.pformat(values42))
    print("31: %s\n", pprint.pformat(values31))


    def is_match_and(rules, sequence):
        sofar = set([0])
        for r in rules:
            rlengths = set()
            for s in sofar:
                rlengths.update(s + x for x in is_match(r, sequence[s:]))
            sofar = rlengths
        return sofar

    def is_match_or(rules, sequence):
        matchlen = set()
        for r in rules:
            matchlen.update(is_match_and(r, sequence))
        return matchlen

    def is_match(n, sequence):
        if not sequence:
            return []
        r = GRAMMAR[n]
        if isinstance(r, str):
            return [1] if sequence.startswith(r) else []
        return is_match_or(r, sequence)

    slist = [ ''.join((values42[0], values42[1], values31[0], values31[1])), 
              ''.join((values42[0], values31[0])) ] 
    #for s in slist:
    #    print(is_match_11(s), s)
    for s in slist:
        print("MATCH 11?" , is_match(11, s), s)
    #sys.exit(0)
    match = []
    for row in lines:
        if not row:
            continue
        elif row[0] in '0123456789':
            continue
        matches = list(sorted(is_match(0, row)))
        found = ""
        if len(row) in matches:
            match.append(row)
            found = "MATCH"
        print(row, len(row), matches, found)

    print("MATCHES", len(match))
