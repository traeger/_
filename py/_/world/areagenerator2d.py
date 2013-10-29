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
from discreateDistribution import DiscreateDistribution
from cellularAutomata import CellularAutomata, CAIter

class AreaGenerator2d(object):
    def __init__(self, seed, areaSize, distribution = [('W',0.4), ('S',0.3)], defaultvalue = 'G'): 
        self.seed = seed;
        self.areaSize = areaSize
        self.area = numpy.zeros((self.GEN_SIZE, self.GEN_SIZE), dtype=int)
        
        # create a map from state-index to state-name
        # create a index-based distribution
        self.statenamemap = []
        self.statenamemap.append(defaultvalue)
        distribution_index = {}; i = 1
        for key, value in distribution:
            self.statenamemap.append(key)
            distribution_index[i] = value
            i += 1
        
        self.distribution = DiscreateDistribution(distribution_index, 0)
        
        self.initCA()
        
    def chunkSeed(self, cx, cy):
        return self.seed * (cy * self.CHUNK_SIZE + cx);
        
    def randomizeChunk(self, cx, cy, chunkmap):
        rnd = Random(self.chunkSeed(cx, cy))
        
        for y in range(0, self.CHUNK_SIZE):
            for x in range(0, self.CHUNK_SIZE):
                chunkmap[x,y] = self.distribution.value(rnd.random());
                
    def toNamedStates(self, chunk_index, chunk_named = 'copy'):
        xs = chunk_index.shape[0]
        ys = chunk_index.shape[1]
        if(chunk_named is 'copy'):
            chunk_named = numpy.chararray((xs,ys))
        for y in range(0, ys):
            for x in range(0, xs):
                chunk_named[x,y] = self.statenamemap[chunk_index[x,y]]
        return chunk_named
                
    def generate(self, cx, cy, area):
        # randomize chunks
        for j in xrange(0, 3):
            for i in xrange(0, 3):
                x = i * self.CHUNK_SIZE
                y = j * self.CHUNK_SIZE
                c = self.ca_tmpchunks[0][x:x+self.CHUNK_SIZE, y:y+self.CHUNK_SIZE]
                self.randomizeChunk(cx + i - 1, cy + j - 1, c)
    
        # let a cellular automata run <code>self.ca_iterations</code> times
        
        itr = CAIter(self.ca, self.ca_tmpchunks[0], self.ca_tmpchunks[1])
        c = itr.next(debug=False, count = self.ca_iterations + 1)
        self.toNamedStates(c[self.CHUNK_SIZE:2*self.CHUNK_SIZE, self.CHUNK_SIZE:2*self.CHUNK_SIZE], chunk)
        
        
