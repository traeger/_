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

import extension

from collections import deque
import threading


def create_event(message_type, data,  dst=[]):
  """
  dst = destination client ids
  """
  return {u'type': message_type, u'dst': dst, u'data': data}


class Dispatcher(object):

  def __init__(self):
    self.__lock = threading.RLock()
    self.__listener_map = {}
    self.__active_queue = 0
    self.__queue = [deque(), deque()]
   
  def add_listener(self, listener, message_type, id=None):
    """adds a listener for a message_type (e.g. ('type', 1) ) to the event manager"""
    if not (message_type, id) in self.__listener_map:
      self.__listener_map[(message_type, id)] = [listener]
    else:
      l = self.__listener_map[(message_type, id)]
      if not listener in l:
        l.append(listener)
        return True
    return False
  
  def remove_listener(self, listener, message_type, id=None):
    """removes the listener for message_type from the event manager if possible"""
    if (message_type, id) in self.__listener_map:
      l = self.__listener_map[(message_type, id)]
      if listener in l:
        l.remove(listener)
        if not l: # list of listeners is empty
          self.__listener_map.pop((message_type, id), None)
        return True
    return False
    
  def remove_listeners_for_client(self, id):
    pass #TODO 
    
  def __queue(self, event):
    """adds the event to the active queue of the event manager"""
    self.__lock.acquire()
    self.__queue[self.__active_queue].append(event)
    self.__lock.release()
          
  def __trigger(self, event):
    """fires the event right away, skipping the queue."""
    self.__process_event(event)
    
  def abort(self, event):
    """removes the event from the active queue. 
    If update is already called, the event cannot be aborted anymore
    """
    self.__lock.acquire()
    q = self.__queue[self.__active_queue]
    if event in q:
      q.remove(event)
    self.__lock.release()
    
  def queue(self, message_type, data, dst=[]):
    """adds the event to the active queue of the event manager"""
    event = create_event(message_type, data, dst)
    self.__queue(event)
    return event
    
  def trigger(self, message_type, data, dst=[]):
    """fires the event right away, skipping the queue."""
    event = create_event(message_type, data, dst)
    self.__trigger(event)
    return event
    
  def update(self):
    """
    processes all events in the queue. 
    
    !DANGER! CALL THIS METHOD IN ONE THREAD ONLY !DANGER!  
    """
    self.__lock.acquire()
    q = self.__queue[self.__active_queue]    
    self.__active_queue += 1 % 2; #switching queues to prevent event loops
    self.__lock.release()
    while q:
      event = q.popleft()
      self.__process_event(event)
      
  def __call_listeners_for_message_type(self, message_type_tuple, event):
    """checks for the message type and calls all listeners"""
    if message_type_tuple in self.__listener_map:
      l = self.__listener_map[message_type_tuple]
      for listener in l: listener(event[u'type'], event[u'data'])
      
  def __process_event(self, event):
    """executes all listeners for the event."""
    message_type = event['type']
    self.__call_listeners_for_message_type((message_type, None), event)
    for i in event['dst']:
      self.__call_listeners_for_message_type((message_type, i), event)
    

dispatcher = Dispatcher()
"""global dispatcher variable"""


def get_dispatcher():
  return dispatcher