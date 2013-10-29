"""
Licensed under The MIT License (MIT)
Copyright (c) 2013 Marco Träger <marco.traeger at googlemail.com>
This file is part of the game _ and the _.py gameserver (https://github.com/traeger/_).

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os, sys
sys.path.append(os.path.join('..','..'))

import numpy
from _.world.chunkgenerator import Chunkgenerator
from _.math.cellularAutomata import CellularAutomata, CAIter

# ca with 3 stats, 0 grass, 1 water, 2 stone
ca = CellularAutomata(['G','W','S'])
ca.addRule({'center':'S', 'countRestrictions': {'W': ('>=',2)}, 'result': 'G'})
ca.addRule({'center':'W', 'countRestrictions': {'S': ('>=',2)}, 'result': 'G'})

ca.addRule({'center':'S', 'countRestrictions': {'S': ('<',2)}, 'result': 'G'})
ca.addRule({'center':'G', 'countRestrictions': {'S': ('>',3)}, 'result': 'S'})

ca.addRule({'center':'W', 'countRestrictions': {'W': ('<',3)}, 'result': 'G'})
ca.addRule({'center':'G', 'countRestrictions': {'W': ('>',4)}, 'result': 'W'})
# no change otherwise

CHUNK_SIZE = 8

chuckGen = Chunkgenerator(200, {'W':0.4, 'S':0.3}, 'G');
chunks = numpy.zeros((CHUNK_SIZE*3, CHUNK_SIZE*3), dtype=numpy.unicode)

# randomize chunks
for cy in xrange(0, 3):
  for cx in xrange(0, 3):
    x = cx * CHUNK_SIZE
    y = cy * CHUNK_SIZE
    chunk = chunks[x:x+CHUNK_SIZE, y:y+CHUNK_SIZE]
    chuckGen.randomizeChunk(cx, cy, chunk)

c = CAIter(ca, chunks)
def n():
  ar = c.next()
  for l in xrange(0, ar.shape[1]):
    print ar[:,l].tostring()
  #print ar
