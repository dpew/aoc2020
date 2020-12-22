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

def splitfoods(line):
    ing, al = line.split('(')

    inglist = list(tokenize(ing, ' '))
    allist = list(tokenize(al, ' ,)'))
    allist.remove("contains")
    return inglist, allist

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
    data = [ d.strip() for d in f.readlines()]

  foods = [] 
  allergy_assoc = {}
  for d in data:
    ingredients, allergens = splitfoods(d)
    foods.append((allergens, set(ingredients)))
    for a in allergens:
      try:
        foodset = allergy_assoc[a]
        foodset.intersection_update(ingredients)
      except KeyError:
        allergy_assoc[a] = set(ingredients)

  foodmap = {}
  while allergy_assoc:
    alergen, foodset = min(allergy_assoc.items(), key=lambda x: len(x[1]))
    if len(foodset) > 1:
        raise ValueError("Bad Allergen %s: %s" % (alergen, foodset))
    ingredient = list(foodset)[0]
    foodmap[ingredient] = alergen
    del allergy_assoc[alergen]
    for k in allergy_assoc.keys():
        allergy_assoc[k].discard(ingredient)

  count = 0
  known = set(foodmap.keys())
  print("KNOWN", known)
  for al, foodset in foods:
    print(foodset.difference(known))
    count += len(foodset.difference(known))

  print(count)
  print(foodmap)
  print(','.join(x[0] for x in sorted(foodmap.items(), key=lambda x: x[1])))
