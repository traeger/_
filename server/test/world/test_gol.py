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

import os, sys
sys.path.append(os.path.join('..','..'))

import numpy

from _.math.cellularAutomata import CellularAutomata, CAIter

# ca with 2 stats
ca = CellularAutomata([0,1])
# a dead (0) cell with exactly 3 living (1) neighbors: lives
ca.addRule({'center':0, 'countRestrictions': {1: ('==',3)}, 'result': 1})
# a living (1) cell with lesser that 2 living (1) neighbors: dies
ca.addRule({'center':1, 'countRestrictions': {1: ('<' ,2)}, 'result': 0})
# a living (1) cell with greater that 2 living (1) neighbors: dies
ca.addRule({'center':1, 'countRestrictions': {1: ('>' ,3)}, 'result': 0})
# no change otherwise

#initital board
clockF = numpy.array([
    [0,0,0,0,0,0],
    [0,0,1,0,0,0],
    [0,0,1,0,1,0],
    [0,1,0,1,0,0],
    [0,0,0,1,0,0],
    [0,0,0,0,0,0],
], dtype=numpy.int)

#create ca-iterator, see Uhr: http://de.wikipedia.org/wiki/Conways_Spiel_des_Lebens
#next board with: clock.next()
clock = CAIter(ca, clockF)

#initital board, see Toad (periode 2): http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
toadF = numpy.array([
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,1,1,1,0],
    [0,1,1,1,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
], dtype=numpy.int)

#create ca-iterator
#next board with: toad.next()
toad = CAIter(ca, toadF)
