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
from noise import snoise2
import math

"""
since the values of the perlin noise are most of the time distributed
in the interval [-1/sqrt(4/n), +1/sqrt(4/n)] (for a n-dim noise),
this values are used to scale the noise variance.

http://www.gamedev.net/topic/293492-perlin-noise-distribution/
"""
PERLIN_V100 = 1.0/(4/2)**0.5
PERLIN_V50 = 0.3 / PERLIN_V100

"""
generate a world-scale noise using
simplex-noise a fast(but approx.) method of perlin-noise
"""

def worldscale(seed, mean = 0.0, v50 = 0.3, v100 = 1.0):
  return WorldNoise(seed, 
    frequency = 10.0 * 1000.0 * 1000.0, # frequency for a 1 pixel = 1m solution 
    mean = mean, v50 = v50, v100 = v100)

def regionscale(seed, mean = 0.0, v50 = 0.3, v100 = 1.0):
  return WorldNoise(seed, 
    frequency = 1000.0 * 10.0,
    mean = mean, v50 = v50, v100 = v100)
    
def localscale(seed, mean = 0.0, v50 = 0.3, v100 = 1.0):
  return WorldNoise(seed, 
    frequency = 100.0,
    mean = mean, v50 = v50, v100 = v100)

class WorldNoise:
  def __init__(self, seed, frequency = 1, octaves = 50, mean = 0.0, v50 = 0.3, v100 = 1.0):
    self.frequency = frequency
    self.octaves = octaves
    self.seed = seed
    
    self.mean = mean
    self.v50  = v50
    self.v100 = v100
    
    # quadratic interpolation
    self.a1 = (self.v50 - PERLIN_V50 * self.v100) / (PERLIN_V50**2 - PERLIN_V50)
    self.a2 = (self.v100 - self.a1)
    
    rnd = Random(self.seed)
    self.xseed = rnd.random() * self.frequency * self.octaves
    self.yseed = rnd.random() * self.frequency * self.octaves
  
  """
  zoom - zoomfactor, 1 := 1m, 1000 := 1km, and so on
  ox - xoffset in the zoom factor, so zoom==10000, ox=10 means a offset of 10000m*10
  oy - yoffset in the zoom factor
  area - 2d numpy array to write the map to
  """
  def generate(self, xo, yo, zoom, area, add=False):
    xs = area.shape[0]
    ys = area.shape[1]
    for y in xrange(0,ys):
      for x in xrange(0,xs):
        v = self[xo+x,yo+y,zoom]
        if(add):
          area[x,y] += v
        else:
          area[x,y] = v
    return area
        
        #area[x,y] = snoise2(
        #  (self.xseed + (xo+x)*scale) / self.frequency,
        #  (self.yseed + (yo+y)*scale) / self.frequency,
        #  self.octaves
        #)
        
  def __getitem__(self, idx):
    x, y, zoom = idx
    v = snoise2(
      (self.xseed + (x)*zoom) / self.frequency,
      (self.yseed + (y)*zoom) / self.frequency,
      self.octaves
    )
    vabs = math.fabs(v / PERLIN_V100)
    wabs = self.a1 * vabs*vabs + self.a2 * vabs
    return math.copysign(wabs, v)
        
  """
  just for tests, discreatize the area via fixed threshholds
  """
  def discretize(self, area):
    xs = area.shape[0]
    ys = area.shape[1]
    for y in xrange(0, ys):
      for x in xrange(0, xs):
        v = area[x,y]
        if  (v <= 0):
          w = 0.0
        else:
          w = v
        area[x,y] = w
