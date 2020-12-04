#!/usr/bin/env python3

import itertools

values=[]
with open("day1.txt") as f:
    values = [int(x) for x in f.readlines()]

for p in itertools.permutations(values, 2):
    # print(p, sum(p))
    if sum(p) == 2020:
        print(p, p[0] * p[1])

for p in itertools.permutations(values, 3):
    # print(p, sum(p))
    if sum(p) == 2020:
        print(p, p[0] * p[1] * p[2])
