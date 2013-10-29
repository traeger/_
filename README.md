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

    -   gevent-websocket
        ```
        clone the branch 'default' from https://bitbucket.org/Jeffrey/gevent-websocket/src
        ```
        and than install it with:
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

*   have fun!
