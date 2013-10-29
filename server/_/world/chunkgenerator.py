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

import numpy
from math.discreateDistribution import DiscreateDistribution
from math.cellularAutomata import CellularAutomata, CAIter

class Chunkgenerator(object):
    CHUNK_SIZE = 8;
    GEN_SIZE = CHUNK_SIZE*3;
    
    def __init__(self, seed, distribution = {'W':0.4, 'S':0.3}, defaultvalue = 'G'): 
        self.seed = seed;
        self.distribution = DiscreateDistribution(distribution, defaultvalue)
        self.initCA()
        
    def initCA(self):
        self.ca = CellularAutomata(['G','W','S'])
        self.ca.addRule({'center':'S', 'countRestrictions': {'W': ('>=',2)}, 'result': 'G'})
        self.ca.addRule({'center':'W', 'countRestrictions': {'S': ('>=',2)}, 'result': 'G'})

        self.ca.addRule({'center':'S', 'countRestrictions': {'S': ('<',2)}, 'result': 'G'})
        self.ca.addRule({'center':'G', 'countRestrictions': {'S': ('>',3)}, 'result': 'S'})

        self.ca.addRule({'center':'W', 'countRestrictions': {'W': ('<',3)}, 'result': 'G'})
        self.ca.addRule({'center':'G', 'countRestrictions': {'W': ('>',4)}, 'result': 'W'})
        
        self.ca_tmpchunks = {}
        self.ca_tmpchunks[0] = numpy.zeros((self.GEN_SIZE,self.GEN_SIZE), dtype=numpy.unicode)
        self.ca_tmpchunks[1] = numpy.zeros((self.GEN_SIZE,self.GEN_SIZE), dtype=numpy.unicode)
        
        self.ca_iterations = 6
        
    def chunkSeed(self, cx, cy):
        # minecraft chunkseed modifications
        rnd = Random(self.seed)
        mx = (rnd.random() / 2) * 2 + 1
        my = (rnd.random() / 2) * 2 + 1
        
        return (cy*(my**self.seed)) + (cx*mx)

    def randomizeChunk(self, cx, cy, chunkmap):
        rnd = Random(self.chunkSeed(cx, cy))
        
        for y in range(0, self.CHUNK_SIZE):
            for x in range(0, self.CHUNK_SIZE):
                chunkmap[x,y] = self.distribution.value(rnd.random());

    def chunk(self, cx, cy, chunk):
        # randomize initial 3x3 chunks
        for j in xrange(0, 3):
            for i in xrange(0, 3):
                x = i * self.CHUNK_SIZE
                y = j * self.CHUNK_SIZE
                c = self.ca_tmpchunks[0][x:x+self.CHUNK_SIZE, y:y+self.CHUNK_SIZE]
                self.randomizeChunk(cx + i - 1, cy + j - 1, c)
    
        # let a cellular automata run <code>self.ca_iterations</code> times
        itr = CAIter(self.ca, self.ca_tmpchunks[0], self.ca_tmpchunks[1])
        c = itr.next(count = self.ca_iterations + 1)
        
        # move the center tmp-chunk to the output
        chunk = c[self.CHUNK_SIZE:2*self.CHUNK_SIZE, self.CHUNK_SIZE:2*self.CHUNK_SIZE]
