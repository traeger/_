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

from _.world.biome import Biome
from _.world.world import World
import numpy
from scipy.misc import toimage

###
# bioms
###
b = Biome.default()
area = numpy.zeros((200,200,3), dtype=numpy.float)
for y in xrange(0, area.shape[1]):
  for x in xrange(0, area.shape[0]):
    area[x,y,:] = b.toColor(b[x/200.0,y/100.0-1.0])
    
toimage(area.transpose()).show()


###
# world gen
###
meterperpixel = 100 * 1000 # 100km
zoom = 2
scale = 1 * (meterperpixel / zoom)

w = World(367598)

area = numpy.zeros((400*zoom,200*zoom,3), dtype=numpy.float)
heights = numpy.zeros((400*zoom,200*zoom), dtype=numpy.float)

w.genBiomeMapColor (0, 0, scale, area)

# ocean
w.genHeightMap(0, 0, scale, heights)
for y in xrange(0, area.shape[1]):
  for x in xrange(0, area.shape[0]):
    if heights[x,y] < 0:
      area[x,y,:] = [0,0,1]
    
toimage(area.transpose()).show()
