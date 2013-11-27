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
  return {u'type': message_type, u'dst': dst, u'data': data}


class Dispatcher(object):

  def __init__(self):
    self.__lock = threading.RLock()
    self.__listener_map = {}
    self.__active_queue = 0
    self.__queue = [deque(), deque()]
   
  def add_listener(self, listener, message_type):
    """adds a listener for a message_type (e.g. ('type', 1) ) to the event manager"""
    if not message_type in self.__listener_map:
      self.__listener_map[message_type] = [listener]
    else:
      l = self.__listener_map[message_type]
      if not listener in l:
        l.append(listener)
        return True
    return False
  
  def remove_listener(self, listener, message_type):
    """removes the listener for message_type from the event manager if possible"""
    if message_type in self.__listener_map:
      l = self.__listener_map[message_type]
      if listener in l:
        l.remove(listener)
        if not l:
          self.__listener_map.pop(message_type, None)
        return True
    return False
    
  def queue_event(self, event):
    """adds the event to the active queue of the event manager"""
    self.__lock.acquire()
    self.__queue[self.__active_queue].append(event)
    self.__lock.release()
    
  def abort_event(self, event):
    """removes the event from the active queue. 
    If update is already called, the event cannot be aborted anymore
    """
    self.__lock.acquire()
    q = self.__queue[self.__active_queue]
    if event in q:
      q.remove(event)
    self.__lock.release()

      
  def trigger_event(self, event):
    """fires the event right away, skipping the queue."""
    self.__process_event(event)
    
  def update(self):
    """processes all events in the queue. """
    self.__lock.acquire()
    q = self.__queue[self.__active_queue]    
    self.__active_queue += 1 % 2; #switching queues to prevent event loops
    self.__lock.release()
    while q:
      event = q.popleft()
      self.__process_event(event)
      
  def __call_listeners_for_message_type(self, message_type, event):
    """checks for the message type and calls all listeners"""
    if message_type in self.__listener_map:
      l = self.__listener_map[message_type]
      for listener in l: listener(event)
      
  def __process_event(self, event):
    """executes all listeners for the event."""
    message_type = event['type']
    self.__call_listeners_for_message_type(message_type, event)
    for i in event['dst']:
      self.__call_listeners_for_message_type((message_type, i), event)


class RemoteListener(object):

  def __init__(self, client_id):
    """creates the remote wrapper for a client connection"""
    from net import get_connection_manager
    self.__registered = False
    self.__ID = client_id
    self.__con_man = get_connection_manager()
    self.__queue = deque()
    extension.get_extension_manager().register_client()

    #TODO register all event types here, the client needs to listen to

    dispatcher.add_listener(self.__callback_to_client, ('MYEVENT', self.__ID))
    
  def __callback_to_client(self, event):
    """sends events from the dispatcher to the client"""
    self.__con_man.send_to_client(self.__ID, event)
    
  def callback_from_client(self, event):
    """receives an event from the client and inserts it into the event queue"""
    #TODO sanatize input here!
    
    #TODO maybe process listener-add/remove-requests here
    if self.__registered:
      dispatcher.queue_event(event)
    else:
      self.__queue.append(event)
    

dispatcher = Dispatcher()
"""global dispatcher variable"""


def get_dispatcher():
  return dispatcher