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

useColor = True

meterperpixel = 100 * 1000 # 1km
zoom = 2
scale = 1 * (meterperpixel / zoom)

w = World(20)

area = numpy.zeros((400*zoom,200*zoom), dtype=numpy.float)
xs = area.shape[0]
ys = area.shape[1]

w.genHeightMap(0, 0, scale, area[0:200*zoom,:])
w.genHeightMap(200*zoom, 0, scale, area[200*zoom:400*zoom,:])
w.discretize(area)

toimage(area.transpose()).show()

# find a good zoom point
for y in xrange(0, ys):
  for x in xrange(0, xs):
    if area[x,y] > 0.4:
      poi = (scale*x,scale*y)
      
for z in [10000, 1000, 100, 10, 1]:
  if not useColor:
    smallarea = numpy.zeros((300,300), dtype=numpy.float)
  else:
    smallarea = numpy.zeros((300,300,3), dtype=numpy.float)
  xs = smallarea.shape[0]
  ys = smallarea.shape[1]
  if not useColor:
    w.genHeightMap(poi[0]/z, poi[1]/z, z, smallarea)
    w.discretize(smallarea)
  else:
    w.genBiomeMapColor(poi[0]/z, poi[1]/z, z, smallarea)
    
  toimage(smallarea.transpose()).show()
