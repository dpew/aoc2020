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

MAXEDGE=(1<<10)
def flip(edgeval):
    '''
    >>> bin(flip(int("1000011111", 2)))
    '0b1111100001'
    >>> bin(flip(int("1000000000", 2)))
    '0b1'
    '''
    b = '{:0{width}b}'.format(edgeval, width=10)
    return int(b[::-1], 2)

class Edge(object):

    def __init__(self, tile, e1, e2):
        self.tile = tile
        self.e1 = e1
        self.e2 = e2
        self.ef1 = e1[::-1] # flipped edge 1
        self.ef2 = e2[::-1] # flippted edge 2

    def __repr__(self):
        return '\n'.join((self.e1,'-'*10,self.ef2))

class Chain(object):

    def __init__(self):
        self.chains = deque()
        self.tiles = set()

class Tile(object):

    def __init__(self, name):
        self.name = name
        self.data = []
        self.rotation = 0
        self.flip = 1

    def set_data(self, data):
        self.data = list(data)
        # always read clockwise
        self.topbottom = Edge(self, self.data[0], self.data[-1][::-1])
        self.leftright = Edge(self, ''.join(d[-1] for d in self.data), ''.join(d[0] for d in self.data[::-1]))

    def get_edge(self, direction):
        d = (direction * self.flip + self.rotation) % 4
        if d == 0:
            return self.topbottom.e1[::self.flip]
        if d == 1:
            return self.leftright.e2[::self.flip]
        if d == 2:
            return self.topbottom.e2[::self.flip]
        if d == 3:
            return self.leftright.e1[::self.flip]
        raise ValueError("bad direction %d" % (direction,))

    @property
    def edges(self):
        return (self.topbottom, self.leftright)

    def __repr__(self):
        return "Tile[r=%d,f=%d] %s:\n%s" % (self.rotation, self.flip, self.name, "\n".join(self.data))


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
        tiledata = [ t.strip() for t in f.readlines()]

    tiles = {}
    tile = None
    data = []
    for t in tiledata:
      if t.startswith("Tile"):
        tile = Tile(list(tokenize(t, " :\n"))[1])
        tiles[tile.name] = tile
        continue
      if t == "":
        tile.set_data(data)
        tile = None
        data = []
        continue
      data.append(t)
    if data:
      tile.set_data(data)

    for k in sorted(tiles.keys()):
        print(tiles[k], end="\n\n")


    edgemap = defaultdict(lambda: list())
    edgeset = set()
    for t in tiles.values():
        for e in t.edges:
            edgemap[e.e1].append(e)
            edgemap[e.e2].append(e)
            edgemap[e.ef1].append(e)
            edgemap[e.ef2].append(e)
            edgeset.add(e)

    cnt = 0
    cmap = defaultdict(lambda: 0)
    for e, l in edgemap.items():
        cmap[len(l)] += 1
    print(cmap)

    def find_adj(edge, seen, direction):
       elist = edgemap[edge]
       direction = (direction + 2) % 4
       for e in elist:
           if e.tile in seen:
               continue
           for flip in (1, -1):
               for rotation in range(4):
                   e.tile.rotation = rotation
                   e.tile.flip = flip
                   if edge == e.tile.get_edge(direction+2):
                       return e.tile.get_edge(direction), e.tile
           #if e.e1 == edge:
           #    return e.e2, e.tile
           #elif e.e2 == edge:
           #    return e.e1, e.tile
           #elif e.ef1 == edge:
           #    return e.ef2, e.tile
           #elif e.ef2 == edge:
           #    return e.ef1, e.tile
           raise ValueError("Bad edge! " + edge)
       return None, None

    # get first file, and spread out in all four directions
    def find_boundary(start_tile, direction):
        moves = defaultdict(lambda: 0)
        seen = set()
        t = start_tile
        ne = t.get_edge(direction)
        seen.add(t)
        moves[direction] += 1
        while True:
            ne, adj = find_adj(ne, seen, direction)
            if adj == None:
                print(moves)
                return t
            moves[direction] += 1
            t = adj
            seen.add(t)

    t0 = list(tiles.values())[0]
    boundary0 = find_boundary(t0, 0)
    boundary1 = find_boundary(t0, 2)
    print("B0", boundary0)
    print("B1", boundary1)
    corners = []
    corners.append(find_boundary(boundary0, 1))
    corners.append(find_boundary(boundary0, 3))
    corners.append(find_boundary(boundary1, 1))
    corners.append(find_boundary(boundary1, 3))
    print(corners)
    r = 1
    for t in corners:
        r = r * int(t.name)
    print(r)

        
    # build unique chains.  Any chains of at least 12 tiles is a candidate
    #chains = []
    #while true:
    #    e = edgeset.pop()
    #    for c in chains:
    #        if c.matchesLeft(e):
    #            if c.matchesRight(e):
#
#                c.addLeft(e)
#        e = edge.pop()
#        chain = Chain()
#        chain.add(e)
#
#    remain = edges.()
#    while len(used)
#    for k, elist in edges.items():
#      for e in elist:
#         add_edge_to_chain(chains, used, e)
#         used.add(e)
