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

import worldNoise
from biome import Biome

from _.constants import *

class World:
    
  def __init__(self, seed):
    self.heightGen = worldNoise.worldscale(seed, mean=0, v50 = WORLD_HEIGHT_HALF, v100=WORLD_HEIGHT_MAX)
    self.regionHeightGen = worldNoise.regionscale(seed, mean=0, v50 = REGION_HEIGHT_HALF, v100=REGION_HEIGHT_MAX)
    self.localHeightGen = worldNoise.localscale(seed, mean=0, v50 = LOCAL_HEIGHT_HALF, v100=LOCAL_HEIGHT_MAX)
    self.moistureGen  = worldNoise.worldscale(2**seed)
    self.biome = Biome.default()
  
  def genHeightMap(self, xo, yo, zoom, area):
    self.heightGen.generate(xo, yo, zoom, area)
    self.regionHeightGen.generate(xo, yo, zoom, area, add=True)
    self.localHeightGen.generate(xo, yo, zoom, area, add=True)
    return area
  
  def genMoistureMap(self, xo, yo, zoom, area):
    return self.moistureGen.generate(xo*3, yo*3, zoom/3, area)
  
  def genBiomeMap(self, xo, yo, zoom, area):
    for y in xrange(0, area.shape[1]):
      for x in xrange(0, area.shape[0]):
        height   = self.heightGen[xo+x,yo+y,zoom]
        moisture = self.moistureGen[xo+x,yo+y,zoom/3]
        
        area[x,y] = self.biome[height, moisture]
  
  def genBiomeMapColor(self, xo, yo, zoom, area):
    for y in xrange(0, area.shape[1]):
      for x in xrange(0, area.shape[0]):
        height   = self.heightGen[xo+x,yo+y,zoom]
        moisture = self.moistureGen[xo+x,yo+y,zoom/3]
        
        area[x,y,:] = self.biomecolor(self.biome[height, moisture])
    
  def biomecolor(self, biometype):
    return self.biome.toColor(biometype)
    
  def discretize(self, area):
    return self.heightGen.discretize(area)
