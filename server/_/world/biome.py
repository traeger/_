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

import numpy
from scipy.spatial import cKDTree

HEIGHT_VARIANCE = 4000.0

"""
http://de.wikipedia.org/wiki/Gebirgsland
"""

class Biome:
  IDX_HEIGHT = 0
  IDX_MOISTURE = 1
  IDX_COLOR = 3
  
  def __init__(self):
    self.biomes = []
    self.fromName = {}
    self.triangulated = False
  
  def addBiome(self, height, moisture, name, color):
    t = (height, moisture, name, numpy.array(color))
    self.fromName[name] = len(self.biomes)
    self.biomes.append( t )
    self.triangulated = False
  
  def triangulate(self):
    self.biomesAr = dict(zip(xrange(0,len(self.biomes)), self.biomes))
    
    # triangulate via height and moisture
    points = map(
      lambda t: (t[Biome.IDX_HEIGHT]/HEIGHT_VARIANCE, t[Biome.IDX_MOISTURE]),
      self.biomes
    )
    points = numpy.array(points)
    self.kdtree = cKDTree(points, leafsize = 3)
    self.triangulated = True
    self.points = points
    
    print "tri ready"
    
  def __getitem__(self, p):
    if p[0] > 6000:
      return self.fromName["Snow"]
    
    if not self.triangulated: self.triangulate()
    nearest = self.kdtree.query((p[0]/HEIGHT_VARIANCE, p[1]), k=1, p=2)
    return nearest[1]
  
  def toColor(self, idx):
    biome = self.biomesAr[idx]
    return biome[Biome.IDX_COLOR]
  
  @classmethod
  def default(self):
    b = Biome()
    
    #
    b.addBiome(100,  0.9, "Tropical Rainforest", [0.0,1.0,0.0])
    b.addBiome(100,  0.4, "Tropical Seasonal Forest", [0.5,1.0,0.0])
    b.addBiome(100, -1.0, "Subtropical Desert", [0.9,0.8,0.0])
    #
    b.addBiome(200,  0.0, "Grassland", [0.4,0.8,0.0])
    #
    b.addBiome(300,  0.8, "Temperate Rain Forest", [0.5,0.9,0.0])
    b.addBiome(300,  0.7, "Temperate Deciduouse Forest", [0.5,0.7,0.0])
    b.addBiome(200, -1.0, "Temperate Desert", [0.8,0.8,0.0])
    #
    b.addBiome(800,  0.9, "Taiga", [0.3,0.3,0.1])
    b.addBiome(800,  0.5, "Schrubland", [0.4,0.4,0.2])
    #
    b.addBiome(6000,  0.8, "Snow", [1.0,1.0,1.0])
    b.addBiome(2000,  0.2, "Tundra", [0.2,0.2,0.0])
    b.addBiome(2000, -0.3, "Barerock", [0.5,0.5,0.5])
    b.addBiome(2000, -1.0, "Scorched", [0.3,0.3,0.3])
    
    b.triangulate()
    return b
