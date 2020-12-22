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
        self._fdata = []
        self._rotation = 0 # clockwise rotations, 90 degrees each
        self._flip = 1
        self.size = 0

    def rotate(self, steps):
        self._rotation = steps % 4
        self._update_data()

    def flip(self, flip):
        if flip not in (-1, 1):
            raise ValueError("Bad flip %s. Must be -1, 1." % (flip,))
        self._flip = flip
        self._update_data()

    def set_data(self, data):
        self.data = deepcopy(data)
        self._update_data()
        self.topbottom = Edge(self, self.data[0], self.data[-1][::-1])
        self.leftright = Edge(self, ''.join(d[-1] for d in self.data), ''.join(d[0] for d in self.data[::-1]))
        return self

    def _update_data(self):
        self._fdata = self.data
        if self._flip == -1:
           self._fdata = flip_matrix(self._fdata)
        for _ in range(self._rotation):
           self._fdata = rotate_matrix(self._fdata)
        # stringify the matrix rows
        self._fdata = [ ''.join(row) for row in self._fdata]

    def get_edge(self, direction):
        '''
            direction = 0, 1, 2, 3.  Represents clockwise rotations
            >>> t = Tile('test').set_data(['0123', '4567', '89ab', 'cdef'])
            >>> t.get_edge(0)
            '0123'
            >>> t.get_edge(1)
            '37bf'
            >>> t.get_edge(2)
            'fedc'
            >>> t.get_edge(3)
            'c840'
            >>> t.rotate(2)
            >>> t.get_edge(0)
            'fedc'
            >>> t.flip(-1)
            >>> t.rotate(0)
            >>> t.get_edge(0)
            '3210'
            >>> t.get_edge(1)
            '048c'
        '''
        direction = direction % 4
        if direction == 0:
            return self._fdata[0]
        elif direction == 1:
            return ''.join(row[-1] for row in self._fdata)
        elif direction == 2:
            return self._fdata[-1][::-1]
        elif direction == 3:
            return ''.join(row[0] for row in reversed(self._fdata))
        
        raise ValueError("bad direction %d" % (direction,))

    @property
    def edges(self):
        return (self.topbottom, self.leftright)

    def __repr__(self):
        return "Tile[r=%d,f=%d] %s:\n%s" % (self._rotation, self._flip, self.name, "\n".join(self._fdata))


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
           if edge in (e.e1, e.e2):
               flip = -1
           else:
               flip = 1
           for rotation in range(4):
                   e.tile.rotate(rotation)
                   e.tile.flip(flip)
                   if edge[::-1] == e.tile.get_edge(direction):
                       return e.tile.get_edge(direction+2), e.tile
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

    # now proceed down and over from the corners
    matrix = []
    left = corners[1]
    edge1 = left.get_edge(2)
    seen = set()
    seen.add(left)
    while edge1 is not None:
        row = []
        print("ROWROWROW", row)
        matrix.append(row)
        t = left
        ne = left.get_edge(1)
        while ne is not None:
            row.append(t)
            ne, t = find_adj(ne, seen, 1)
            seen.add(t)
        edge1, left = find_adj(edge1, seen, 2)
        seen.add(left)
    
        
    for row in matrix:
        for e in range(10):
            for t in row:
                print(''.join(t._fdata[e]), end='|')
            print()
        print('-'*120)


    newmatrix = []
    for row in matrix:
        for e in range(10):
            newmatrix.append(list(''.join(t._fdata[e]) for t in row))

    fullmatrix = deepcopy(newmatrix)
    for row in newmatrix:
        print(''.join(row))

    monster = [
'                  # ',
'#    ##    ##    ###',
' #  #  #  #  #  #   '
]

    def getpos(matrix, pos):
        try:
            matrix[pos[1]][pos[0]]
        except IndexError:
            return '.'

    def setpos(matrix, pos, c):
        matrix[pos[1]][pos[0]] = c

    def intersect_monster(matrix, pos):
        for y, mr in enumerate(monster):
            for x, mv in enumerate(mr):
                mpos = addpos((x, y), pos)
                if mv == '#' and getpos(matrix, mpos) != '#':
                    return False
        print("FOUND MONSTER")
        return True

    def setmonster(matrix, pos):
        for y, mr in enumerate(monster):
            for x, mv in enumerate(mr):
                mpos = addpos((x, y), pos)
                if mv == '#':
                    setpos(matrix, mpos, 'O')

    cnt = 0
    for flip in (-1, 1):
        for rotate in range(4):
            for y in range(len(newmatrix)):
                for x in range(len(newmatrix)):
                    if intersect_monster(newmatrix, (x, y)):
                        cnt += 1
                        setmonster(newmatrix, (x, y))
            newmatrix = rotate_matrix(newmatrix)
        newmatrix = flip_matrix(newmatrix)

    print('='*120)
    for row in newmatrix:
        print(''.join(row))

    roughness = 0
    for row in newmatrix:
        roughness += sum(1 if v == '#' else 0 for v in row)
    print(cnt, roughness)
    # build unique chains.  Any chains of at least 12 tiles is a candidate

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
