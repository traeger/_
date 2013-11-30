"""
Licensed under The MIT License (MIT)
Copyright (c) 2013 Marco Traeger <marco.traeger at googlemail.com>
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

import time, thread
from _ import dispatcher, extension, net

__dispatcher = dispatcher.get_dispatcher()
__manager = extension.get_extension_manager()
    
def add_extension(name, clazz):
  __manager.add_extension(name, clazz)
  
def main_loop():
  #main game loop:
  while True:
    __dispatcher.update()
    time.sleep(0.1)

def start(port):
  thread.start_new_thread(main_loop,())
  net.start_server(port)