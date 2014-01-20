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

from random import Random
import sys

import numpy
from _.mathutils.discreateDistribution import DiscreateDistribution
from _.mathutils.cellularAutomata import CellularAutomata, CAIter
from _.world.world import World
from _.constants import *

GEN_SIZE = CHUNK_SIZE*3;

class Chunkgenerator(object):
    def __init__(self, seed, distribution={}, default='G'):
        self.world = World(seed)
        self.seed = seed
        self.initCA()
        self.tmpchunk = numpy.zeros((GEN_SIZE,GEN_SIZE), dtype=numpy.float)
        
    def initCA(self):
        self.ca = CellularAutomata(['G','W','S'])
        self.ca.addRule({'center':'S', 'countRestrictions': {'W': ('>=',2)}, 'result': 'G'})
        self.ca.addRule({'center':'W', 'countRestrictions': {'S': ('>=',2)}, 'result': 'G'})

        self.ca.addRule({'center':'S', 'countRestrictions': {'S': ('<',2)}, 'result': 'G'})
        self.ca.addRule({'center':'G', 'countRestrictions': {'S': ('>',3)}, 'result': 'S'})

        self.ca.addRule({'center':'W', 'countRestrictions': {'W': ('<',3)}, 'result': 'G'})
        self.ca.addRule({'center':'G', 'countRestrictions': {'W': ('>',4)}, 'result': 'W'})
        
        self.ca_tmpchunks = {}
        self.ca_tmpchunks[0] = numpy.zeros((GEN_SIZE,GEN_SIZE), dtype='|S1')
        self.ca_tmpchunks[1] = numpy.zeros((GEN_SIZE,GEN_SIZE), dtype='|S1')
        
        self.ca_iterations = 6
        
    def chunkSeed(self, cx, cy):
        # minecraft chunkseed modifications
        rnd = Random(self.seed)
        mx = int ( (rnd.random() / 2) * 2 + 1 )
        my = int ( (rnd.random() / 2) * 2 + 1 )
        
        return (cy*( pow(my, self.seed, sys.maxint) )) + (cx*mx)

    def chunk(self, cx, cy, chunk):
        # pick initial 3x3 chunks
        self.world.genHeightMap((cx-1)*CHUNK_SIZE, (cy-1)*CHUNK_SIZE, 1, self.tmpchunk)
        for y in xrange(0, GEN_SIZE):
            for x in xrange(0, GEN_SIZE):
                v = self.tmpchunk[x,y]
                if v <= 0:
                    w = 'W'
                elif v <= 0.4:
                    w = 'G'
                else:
                    w = 'S'
                self.ca_tmpchunks[0][x,y] = w
    
        # let a cellular automata run <code>self.ca_iterations</code> times
        #itr = CAIter(self.ca, self.ca_tmpchunks[0], self.ca_tmpchunks[1])
        #c = itr.next(count = self.ca_iterations + 1)
        c_height  = self.tmpchunk
        c_terrain = self.ca_tmpchunks[0]
        
        # move the center tmp-chunk to the output
        # terrain
        chunk[CHUNK_DIM_TERRAIN,:,:] = c_terrain[CHUNK_SIZE:2*CHUNK_SIZE, CHUNK_SIZE:2*CHUNK_SIZE]
        # height
        chunk[CHUNK_DIM_HEIGHT,:,:]  = c_height [CHUNK_SIZE:2*CHUNK_SIZE, CHUNK_SIZE:2*CHUNK_SIZE]
        # objects
        rnd = Random(self.chunkSeed(cx,cy))
        for y in xrange(0, CHUNK_SIZE):
            for x in xrange(0, CHUNK_SIZE):
                v = rnd.random()
                if v > 0.99:
                    w = 'T'
                else:
                    w = '_'
                chunk[CHUNK_DIM_OBJECTS,x,y] = w
        
