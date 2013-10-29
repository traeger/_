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
from noise import pnoise2, snoise2

from scipy.misc import toimage

meterperpixel = 100.0 * 1000.0 # 100km
zoom = 2
scale = 1.0 * (meterperpixel / zoom)

rnd = Random(20)
xo = rnd.random() * 100000 * zoom
yo = rnd.random() * 100000 * zoom

area = numpy.zeros((200*zoom,400*zoom), dtype=numpy.float)
xs = area.shape[1]
ys = area.shape[0]
octa = 10
freq = 10.0 * 1000.0 * (1000.0) # 10.000km
for y in xrange(0, ys):
  for x in xrange(0, 200*zoom):
    area[y,x] = snoise2((scale * (xo+x)) / freq, (scale * (yo+y)) / freq, octa)
for y in xrange(0, ys):
  for x in xrange(200*zoom, 400*zoom):
    area[y,x] = snoise2((scale * (xo+x)) / freq, (scale * (yo+y)) / freq, octa)
    
area2 = numpy.zeros((200*zoom,400*zoom), dtype=numpy.float)
for y in xrange(0, ys):
  for x in xrange(0, xs):
    if  (area[y,x] < 0.1):
      area2[y,x] = 0.1
    elif(area[y,x] < 0.4):
      area2[y,x] = 0.4
    elif(area[y,x] < 0.6):
      area2[y,x] = 0.6
    else:
      area2[y,x] = 1

toimage(area2).show()
