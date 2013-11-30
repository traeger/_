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

sys.path[0] = os.path.join(sys.path[0], 'server')
print sys.path

from _ import game
from _.extension import Extension
from _.extensions.base import ExtensionBase

import logging
logger = logging.getLogger(__name__)

# logging dest. and level
logging.basicConfig(level=logging.DEBUG)

class ExtensionTest(Extension):
  def on_setup(self):
    logger.info('test: on_setup')
    self.exBase = self.extensions['base']
    
  def on_start(self):
    self.send_initial()
    
  def send_initial(self):
    self.exBase.send_move_position()
    for cy in xrange(-3,3+1):
      for cx in xrange(-3,3+1):
        self.exBase.send_chunk(
          cx + self.exBase.player.pc[0],
          cy + self.exBase.player.pc[1]
        )
        
game.add_extension('base', ExtensionBase)
game.add_extension('test', ExtensionTest)
game.start(10000)