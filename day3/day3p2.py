#!/usr/bin/env python3

import os
import sys
from functools import reduce

# create absolute mydir
mydir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(mydir, '../lib'))

from advent import *
from intcode import *

class Grid(object):

    def __init__(self, grid):
        self.grid = list(grid)
        self.gwidth = len(self.grid[0])
        self.pos = (0,0)
        self.count = 0

    def move(self, pos):
        self.pos = addpos(self.pos, pos)
        print(self.pos, self.get(self.pos))
        return self.get(self.pos)

    def get(self, pos):
        x, y = pos[0] % (self.gwidth - 1), pos[1]
        return self.grid[y][x]

if __name__ == '__main__':
    with open('day3.txt') as f:
        grid = Grid(f.readlines())
    counts = []
    for slope in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
        grid.pos = (0, 0)
        count = 0
        while True:
            try:
                count += 1 if '#' == grid.move(slope) else 0
            except IndexError:
                counts.append(count)
                print(slope, count, grid.pos)
                break
    print(reduce(lambda x,y: x*y, counts))

    
