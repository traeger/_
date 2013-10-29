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

import json

import logging
logger = logging.getLogger(__name__)

class ServerWrapper():
  def __init__(self, server):
    self.server = server
    self.msgHandler = {}
    
  """
  send a message through the websocket
  """
  def send(self, msgtype, data):
    # the message is expected to be a json string
    # of the form: {type: MSGTYPE, data: MSGDATA}
    jsonMsg = json.dumps({u'type': msgtype, u'data': data})
    logger.info('send:' + jsonMsg)
    self.server.send(jsonMsg)
  
  def on_message(self, jsonMsg):
    # the message is expected to be a json string
    # of the form: {type: MSGTYPE, data: MSGDATA}
    msg = json.loads(jsonMsg)
    logger.info('recieved: + ' + str(msg))
    
    msgtype = msg[u'type']
    msgdata = msg[u'data']
    if not msgtype in self.msgHandler:
      self.on_unknown_message_type(msgtype, msgdata)
      return
    
    handler = self.msgHandler[msgtype]
    handler(msgdata)
    
  def on_unknown_message_type(self, msgtype, msgdata):
    logger.info('unkown message type: ' + str(msgtype) + ' msgdata: ' + str(msgdata))
    
  def addMessageHandler(self, msgtype, message_handler):
    self.msgHandler[msgtype] = message_handler
    
  def sleep(self, time):
    self.server.sleep(time)

class ExtensionManager():
  def __init__(self):
    self.extensions = {}
  
  def bindServer(self, serverImpl, port):
    outer = self
    class Server(serverImpl):
      # called when an connection is created and open
      def on_open(self):
        # create our message dispatcher
        self.dispatcher = ServerWrapper(self)
        
        # create extension instances
        self.extensions = {}
        for k in outer.extensions:
          self.extensions[k] = outer.extensions[k](self, self.dispatcher)
        
        # on setup
        for k in outer.extensions:
          self.extensions[k].on_setup()
          
        # on connect
        for k in outer.extensions:
          self.extensions[k].on_connect()
      
      def on_message(self, msg):
        self.dispatcher.on_message(msg)
        
    Server.bindOnPort(Server, port)
    
  def addExtension(self, name, extensionName):
    self.extensions[name] = extensionName

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
