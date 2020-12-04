#!/usr/bin/env python3

import itertools

class PWord(object):
    def __init__(self, mn, mx, letter, pword):
        self.mn = mn
        self.mx = mx
        self.letter = letter
        self.pword = pword

    def validate(self):
        cnt = 0
        for x in self.pword:
            if self.letter == x:
                cnt += 1
        if cnt < self.mn or cnt > self.mx:
            return False
        return True

    def __repr__(self):
        return "%d-%d %s: %s" % (self.mn,  self.mx, self.letter, self.pword)

def ppaword(line):
    x = line.split()
    y = x[0].split('-')
    
    return PWord(int(y[0]), int(y[1]), x[1][0], x[2])

values=[]
with open("day2.txt") as f:
    values = [ ppaword(x) for x in f.readlines() ]

cnt=0
for v in values:
    if v.validate():
        cnt+=1

print(cnt, len(values)) 
