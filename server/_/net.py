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

import geventwebsocket
import json
import client

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ConnectionManager(object):

  def __init__(self):
    self.__con = {}
    self.__remote_listener = {}
    self.__counter = 0


  def add_connection(self,  client_protocol):
    """
    client_protocol - socket abstraction
      send_message(UString)
    """
    self.__counter += 1
    self.__con[self.__counter] = client_protocol
    self.__remote_listener[self.__counter] = client.RemoteListener(self.__counter)
    return self.__counter

  def remove_connection(self, client_id):
    if client_id in self.__con:
      del self.__con[client_id]
    if client_id in self.__remote_listener:
      self.__remote_listener[client_id].close()
      del self.__remote_listener[client_id]

  def send_to_client(self, client_id, type, data):
    if client_id in self.__con:
      self.__con[client_id].send_message(json.dumps({'type':type, 'data': data}))

  def message_from_client(self, client_id, message):
    if client_id in self.__remote_listener:
      json_message = json.loads(message)
      self.__remote_listener[client_id].callback_from_client(json_message['type'], json_message['data'])

con_man = ConnectionManager()
def get_connection_manager():
  return con_man

class ClientProtocol(geventwebsocket.protocols.base.BaseProtocol):

  def __init__(self, app):
    self.__client_id = 0
    self._app = app

  def on_open(self):
    self.__client_id = con_man.add_connection(self)

  def on_message(self, message):
    logger.info(message)
    con_man.message_from_client(self.__client_id, message)

  def on_close(self):
    con_man.remove_connection(self.__client_id)

  def send_message(self, message):
    self._app.ws.send(message)


class ServerSocket(geventwebsocket.WebSocketApplication):

  def build_protocol(self):
    return ClientProtocol(self)
  
  @classmethod
  def start(cls, port):
    s = geventwebsocket.WebSocketServer(
      ('', port),
      geventwebsocket.Resource({'/': ServerSocket})
    )
    s.serve_forever()