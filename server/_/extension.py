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

from net import ServerSocket

import thread
import logging
logger = logging.getLogger(__name__)


class ExtensionManager():

  def __init__(self):
    self.extensions = {}
  
  def bindServer(self, port):
    thread.start_new_thread(ServerSocket.start(port))

  def addExtension(self, name, extension_name):
    self.extensions[name] = extension_name

class Extension:
  def __init__(self, server, dispatcher):
    self.server = server
    self.dispatcher = dispatcher
    
  def on_setup(self):
    #fallback, if not defined by the implementing class
    logger.debug('on_setup not defined')
    pass
  
  def on_connect(self):
    #fallback, if not defined by the implementing class
    logger.debug('on_connect not defined')
    pass
  
  def on_message(self, msgtype, msgdata):
    #fallback, if not defined by the implementing class
    logger.debug('on_message not defined, message: ' + str(msgtype) + ':' + str(msgdata))
    pass
    
  def addMessageHandler(self, msgtype, message_handler):
    self.dispatcher.addMessageHandler(msgtype, message_handler)
    
  def sleep(self, time):
    self.server.sleep(time)
    
  def send(self, msgtype, msgdata):
    self.dispatcher.send(msgtype, msgdata)
    
  @property
  def extensions(self):
    return self.server.extensions

extension_manager = ExtensionManager()
"""global extensionManager variable"""


def get_extension_manager():
  return extension_manager