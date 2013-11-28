import dispatcher
import extension
from collections import deque

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ClientManager:
  __dispatcher = dispatcher.get_dispatcher()
  __extensionManager = extension.get_extension_manager()

  def login(self, user, password, id, remoteListener):
    self.__extensionManager.create_extension(user, id, remoteListener)
    
    return True
    
  def remove_client(self, id):
    pass #TODO
  
client_manager = ClientManager()
def get_client_manager():
  return client_manager

class RemoteListener(object):
  __dispatcher = dispatcher.get_dispatcher()

  def __init__(self, client_id):
    """creates the remote wrapper for a client connection"""
    from net import get_connection_manager
    self.__registered = False
    self.__ID = client_id
    self.__con_man = get_connection_manager()
    self.__queue = deque()
    #extension.get_extension_manager().register_client()

    #TODO register all event types here, the client needs to listen to

    #dispatcher.add_listener(self.__callback_to_client, ('MYEVENT', self.__ID))
    
  def __callback_to_client(self, type, data):
    """sends events from the dispatcher to the client"""
    self.__con_man.send_to_client(self.__ID, type, data)
    
  def register(self, type):
    self.__dispatcher.add_listener(self.__callback_to_client, type, self.__ID)
    
  def close(self):
    """ called by net when the connection to this client is closed """
    client_manager.remove_client(self.__ID)
    self.__dispatcher.remove_listeners_for_client(self.__ID)
    
  def callback_from_client(self, type, data):
    logger.debug("from client: " + str(type) + " data: " + str(data))
  
    """receives an event from the client and inserts it into the event queue"""
    #TODO sanatize input here!
    
    if type == u'login' and not self.__registered:
      user = data['user']
      password = data['password']
      self.__registered = client_manager.login(user, password, self.__ID, self)
      if self.__registered:
        self.__deque()
    
      return
    
    #TODO maybe process listener-add/remove-requests here
    if self.__registered:
      self.__dispatcher.enqueue(type, data, [self.__ID])
    else:
      self.__queue.append((type, data, [self.__ID]))
      
  def __deque(self):
    """ deques __queue into the event system """
    for (type, data, ids) in self.__queue:
      self.__dispatcher.enqueue(type, data, ids)
    self.__queue.clear()
    del self.__queue