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

import dispatcher

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ExtensionManager:
  def __init__(self):
    self.__extensions = {}

  def create_extension(self, user, id, remoteListener):
    logger.info("creating extension for " + str(user) + " with id " + str(id) + "...")
  
    es = {}
    for name, ext in self.__extensions.iteritems():
      e = ext(user,id,remoteListener) # merken zum loeschen
      es[name] = e
    print es
      
    for e in es.itervalues():
      e.extensions = es
    for e in es.itervalues():
      e.on_setup()
    for e in es.itervalues():
      e.on_start()
      
    logger.info("extension created for " + str(user) + " with id " + str(id))
    
  def add_extension(self, name, extension_name):
    self.__extensions[name] = extension_name

extension_manager = ExtensionManager()
def get_extension_manager():
  return extension_manager

class Extension:
  def __init__(self, user,id,remoteListener):
    self.__user = user
    self.__id = id
    self.__d = dispatcher.get_dispatcher()
    self.__remoteListener = remoteListener  
    
  def add_client_listener(self, type):
    self.__remoteListener.register(type)
  
  def add_listener(self, listener, type):
    self.__d.add_listener(listener, type, self.__id)
    
  def add_listener_global(self, listener, type):
    self.__d.add_listener(listener, type)
    
  def send(self, type, data):
    self.__d.enqueue(type, data, [self.__id])
    
  def send_global(self, type, data):
    self.__d.enqueue(type, data)

  def on_setup(self):
    #fallback, if not defined by the implementing class
    logger.debug('on_setup not defined')
    pass
    
  def on_start(self):
    #fallback, if not defined by the implementing class
    logger.debug('on_start not defined')
    pass

  def on_destroy(self):
    #fallback, if not defined by the implementing class
    logger.debug('on_destroy not defined')
    pass
    
  def on_save(self):
    #fallback, if not defined by the implementing class
    logger.debug('on_save not defined')
    pass