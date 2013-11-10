import numpy
import math

from _.constants import *

class Chunk:
  def __init__(self):
    self.heights = numpy.zeros((CHUNK_SIZE, CHUNK_SIZE), dtype=numpy.int)
    self.areadata = numpy.zeros((2, CHUNK_SIZE, CHUNK_SIZE), dtype='|S1')
    
    # tmp
    self.TMP_heightsdiff = numpy.zeros((CHUNK_SIZE, CHUNK_SIZE), dtype='|S1')
    
  def __getitem__(self, idx):
    if   idx == CHUNK_DIM_TERRAIN:
      return self.areadata[0]
    elif idx == CHUNK_DIM_OBJECTS:
      return self.areadata[1]
    elif idx == CHUNK_DIM_HEIGHT:
      return self.heights
    
  def __setitem__(self, idx, value):
    self[idx][:,:] = value
    
  def calcHeightDiffs(self):
    """
    convert height-map from actual "global values" to delta "local values"
    """
    heights = self[CHUNK_DIM_HEIGHT]
    height = self[CHUNK_DIM_HEIGHT][0,0]
    for y in xrange(0, CHUNK_SIZE):
      for x in xrange(0, CHUNK_SIZE):
        v = heights[x,y] - height
        if   v == 0:
          w = '0'
        elif v < 0:
          w = chr(97 - v - 1)
        else:
          w = chr(65 + v - 1)
        self.TMP_heightsdiff[x,y] = w
    return self.TMP_heightsdiff
    
  def asDict(self):
    height = self[CHUNK_DIM_HEIGHT][0,0]
    heightdiffs = self.calcHeightDiffs()
    
    print self[CHUNK_DIM_HEIGHT].ravel(order='C')
    return {
      'height': str(height),
      'terrain':  self[CHUNK_DIM_TERRAIN].ravel(order='C').tostring(),
      'heights' : heightdiffs.ravel(order='C').tostring(),
      'objects':  self[CHUNK_DIM_OBJECTS].ravel(order='C').tostring(),
    }