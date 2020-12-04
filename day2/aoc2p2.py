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
        if self.pword[self.mn-1] == self.letter:
            cnt+=1
        if self.pword[self.mx-1] == self.letter:
            cnt+=1
        return cnt==1

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
