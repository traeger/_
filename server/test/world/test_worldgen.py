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
from random import Random

from scipy.misc import toimage
from _.world.world import World

import matplotlib

meterperpixel = 100 * 1000 # 100km
zoom = 2
scale = 1 * (meterperpixel / zoom)

w = World(367598)

area = numpy.zeros((400*zoom,200*zoom,3), dtype=numpy.float)
heights = numpy.zeros((400*zoom,200*zoom), dtype=numpy.float)
biomes = numpy.zeros((400*zoom,200*zoom), dtype=numpy.int)

w.genHeightMap(0, 0, scale, heights)
w.genBiomeMap (0, 0, scale, biomes)

w.discretize(area[:,:,0])
w.discretize(area[:,:,1])
# biomes
for y in xrange(0, area.shape[1]):
  for x in xrange(0, area.shape[0]):
    v = biomes[x,y]
    area[x,y,:] = w.biomecolor(v)
    
#matplotlib.colors.rgb_to_hsv(area)
#for y in xrange(0, area.shape[1]):
#  for x in xrange(0, area.shape[0]):
#      area[x,y,2] = heights[x,y]
#
#matplotlib.colors.hsv_to_rgb(area)
#

## biomes
for y in xrange(0, area.shape[1]):
  for x in xrange(0, area.shape[0]):
    if heights[x,y] < 0:
      area[x,y,:] = [0,0,1]
    
toimage(area.transpose()).show()
