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

from gevent import sleep
import geventwebsocket as gws

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class WebSocketServer(gws.WebSocketApplication):  
  """
  send a message through the websocket
  """
  def send(self, msg):
    self.ws.send(msg)
    
  def sleep(self, time):
    sleep(time)
    
  @classmethod
  def bindOnPort(self, impl, port):
    webSocketServer = gws.WebSocketServer(
      ('', port),
      gws.Resource({'/': impl})
    )
    webSocketServer.serve_forever()
