_
=

the game _ (called 'blank'). A gameserver _.py and a gameclient _.js

install 
-------

*   python 2.7.5 and the scipy-stack
    http://www.scipy.org/install.html (http://continuum.io/downloads works fine for me)
    (use suitable setup for your system 32bit/64bit)
  
*   install the following python modules
    -   noise (1.2.1 works fine)
        ```
        $ pip install noise
        ```

    -   gevent-websocket (https://bitbucket.org/Jeffrey/gevent-websocket/)
        ```
        clone the branch 'default' from https://bitbucket.org/Jeffrey/gevent-websocket/src
        ```
        and then install it with:
        ```
        $ python setup.py install
        ```
    
        IMPORTANT NOTE
        ` $ pip install gevent-websocket ` wont work at the time this doc is written! 
        since the pip version is only 0.3.6 and does not support a non-blocking message recieve.

*   start the _ gameserver _.py with
    ```
    $ python _.py
    ```

*   open the `index.html` in any browser to start the client

*   move with `W A S D`, have fun!

world generation
----------------

### ingame view

A screenshot of the ingame view in the javascript client _.js

![alt text](https://raw.github.com/traeger/_/master/images/worldgen_example_02.png "(imageview)")

(the tileset licenses are listed in client/static/tilesets/LICENSE)

### biome generation

The world generation can be tested with
```
cd server/test/world
python test_worldgen.py
```
which generates a view on a part(40,000 km x 20,000 km) of the generated world

![alt text](https://raw.github.com/traeger/_/master/images/worldgen_example_01.png "(biomes of the world)")

(biomes of the world, 1pixel=100km, yellow=desert, lightgreen/brown=jungle, green=grass, gray=barerock, darkgray=tundra, white=snow, blue=ocean)

