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

import numpy

class CellularAutomata(object):
    def __init__(self, states):
        self.states = states
        self.init_TMP_statehistogram()
        self.rules = []
            
    def addRule(self, rule):
        self.rules.append((
            rule['center'],
            rule['countRestrictions'],
            rule['result']
        ))
        
    """
    Apply the ca-rules cell-wise to the <code>sourceGrid</code>. The result is stored in
    the <code>targetGrid</code>.
    """
    def apply(self, sourceGrid, targetGrid, border):
        xs = sourceGrid.shape[0]
        ys = sourceGrid.shape[1]
        for y in range(border,ys-border):
            for x in range(border,xs-border):
                targetGrid[x,y] = self.applyForCell(sourceGrid, x, y)
    
    def applyForCell(self, sourceGrid, x, y):
        # cell (x,y) and neighbors
        local = sourceGrid[x-1:x+2, y-1:y+2]
        
        # create a state histogram for all neighbors of (x,y)
        self.reset_TMP_statehistogram()
        for i in range(0,9):
            self._TMP_statehistogram[local.flat[i]] += 1
        self._TMP_statehistogram[local[1,1]] -= 1
        
        # check each rule - if a rule fit: apply the rule-result 
        for center, countRestrictions, result in self.rules:
            if not (center == local[1,1]):
                continue
            if not (self._checkHistogramFit(self._TMP_statehistogram, countRestrictions)):
                continue
            return result
        # if no rule fit, the cell will stay unchanged
        return local[1,1]
    
    def init_TMP_statehistogram(self):
        self._TMP_statehistogram = {}
        for state in self.states:
            self._TMP_statehistogram[state] = 0
    
    def reset_TMP_statehistogram(self):
        for state in self._TMP_statehistogram.iterkeys():
            self._TMP_statehistogram[state] = 0
           
    def _checkHistogramFit(self, histogram, counts):
        for i in counts:
            v = histogram[i]
            op = counts[i][0]
            c  = counts[i][1]
            if   op   == '==':
                if not (v == c): return False
            elif op   == '<':
                if not (v <  c): return False
            elif op   == '>':
                if not (v >  c): return False
            elif op   == '<=':
                if not (v <= c): return False
            elif op   == '>=':
                if not (v >= c): return False
            elif op   == '!=':
                if not (v != c): return False
            else:
                raise Exception('checkHistogramFit operator unkown: "' + op + '", use one of ==,!=,<=,>=,<,>.')
        return True

class CAIter(object):
    def __init__(self, ca, sourceGrid, targetGrid = 'copy'):
        self.ca = ca
        if targetGrid is 'copy':
            targetGrid = sourceGrid.copy()
        self.g = [sourceGrid, targetGrid]
        self.step = 0
    
    def next(self, count = 1):
        if(count == 1):
            c1 = self.g[(self.step  )%2]
            c2 = self.g[(self.step+1)%2]
            self.ca.apply(c1,c2,self.step+1)
            self.step += 1
            return c1
        else:
            for i in xrange(0,count):
                c1 = self.next()
            return c1
