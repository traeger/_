﻿"""
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

import string
import numpy

from _.extension import Extension
from _.world.chunkgenerator_world import Chunkgenerator
import _.player.player as player
from _.constants import *

import logging
logger = logging.getLogger(__name__)

VIEW_CHUNKSBUFFER_X = 3
VIEW_CHUNKSBUFFER_Y = 6

class ExtensionBase(Extension):
  def on_setup(self):
    self.chuckGenerator = Chunkgenerator(367598)
    self.TMP_chunk = numpy.zeros((CHUNK_DIMS, CHUNK_SIZE, CHUNK_SIZE), dtype='|S1')
    self.p = player.randomizeStartLocation()
    
    # register message handler
    self.addMessageHandler('move_delta', self.handle_move_delta)
    
  @property
  def pc(self):
    return (self.p[0] // CHUNK_SIZE, self.p[1] // CHUNK_SIZE)
    
  def send_chunk(self, cx, cy):
    self.chuckGenerator.chunk(cx, cy, self.TMP_chunk)
    data = {
      'cx': cx,
      'cy': cy,
      'chunkdata': {
        'terrain': self.TMP_chunk[CHUNK_DIM_TERRAIN].ravel(order='C').tostring(),
        'height' : self.TMP_chunk[CHUNK_DIM_HEIGHT] .ravel(order='C').tostring(),
        'objects': self.TMP_chunk[CHUNK_DIM_OBJECTS].ravel(order='C').tostring(),
      }
    }
    self.send('chunk', data)
    
  def send_move_position(self):
    data = {
      'x': self.p[0],
      'y': self.p[1]
    }
    self.send('move_position', data)
    
  def handle_move_delta(self, direction):
    dx = direction['x']
    dy = direction['y']
  
    # cheat protection
    if abs(dx) > 1 or abs(dy) > 1:
      logger.warn(str(direction))
      return
    if dx != 0 and dy != 0:
      logger.warn(str(direction))
      return
    
    cx = self.p[0] // CHUNK_SIZE
    cy = self.p[1] // CHUNK_SIZE
    mx = self.p[0] - cx * CHUNK_SIZE
    my = self.p[1] - cy * CHUNK_SIZE
    minth = 0
    maxth = CHUNK_SIZE - 1
    
    # change position and send it
    self.p = (self.p[0] + dx, self.p[1] + dy)
    self.send_move_position()
    
    # send chunks if in range
    if dx < 0 and mx <= minth:
      for c in xrange(-VIEW_CHUNKSBUFFER_Y,VIEW_CHUNKSBUFFER_Y+1):
        self.send_chunk(cx-VIEW_CHUNKSBUFFER_X, cy+c)
    if dx > 0 and mx >= maxth:
      for c in xrange(-VIEW_CHUNKSBUFFER_Y,VIEW_CHUNKSBUFFER_Y+1):
        self.send_chunk(cx+VIEW_CHUNKSBUFFER_X, cy+c)
    if dy < 0 and my <= minth:
      for c in xrange(-VIEW_CHUNKSBUFFER_X,VIEW_CHUNKSBUFFER_X+1):
        self.send_chunk(cx+c, cy-VIEW_CHUNKSBUFFER_Y)
    if dy > 0 and my >= maxth:
      for c in xrange(-VIEW_CHUNKSBUFFER_X,VIEW_CHUNKSBUFFER_X+1):
        self.send_chunk(cx+c, cy+VIEW_CHUNKSBUFFER_Y)