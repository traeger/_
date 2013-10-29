--
-- CellularAutomata
--
1) a simple test, on Conway's Game of Life

a simple can be started with (on a commandline in the current folder)
    python -i world/test_gol.py
  
and than by typing multible times:
    toad.next()
  
this should look like:
    [PATH_TO_THIS_FOLDER]>python -i world/test_gol.py
    >>> toad.next()
    step: 0
    
    array([[0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 1, 1, 1, 0],
           [0, 1, 1, 1, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0]])
    >>> toad.next()
    step: 1
    
    array([[0, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 0, 0],
           [0, 1, 0, 0, 1, 0],
           [0, 1, 0, 0, 1, 0],
           [0, 0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 0]])
    >>>
    
which simulates the Toad (periode 2), see http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life.
The CA-rules and the initial field ca be edited by changing 'test_gol.py' or copy and modify it..