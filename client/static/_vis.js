/*
Licensed under The MIT License (MIT)
Copyright (c) 2013 Marco Träger <marco.traeger at googlemail.com>
This file is part of the game _ and the _.py gameclient (https://github.com/traeger/_).

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
*/

_vis = new function() { var _vis = this;
    var is = function(blockid, is, not) {
        if (is) { for (var key in is) {
            if (is[key] != blockid) return false; 
        }}
        if (not) { for (var key in not) {
            if (not[key] == blockid) return false; 
        }}
        return true;
    }

    _vis.tileVariationForWall = function(cc, c0, c1, c2, c3, c4, c5, c6, c7, swap) {
        if (swap) {
            return _vis.tileVariationForWall(true, c0!=cc, c1!=cc, c2!=cc, c3!=cc, c4!=cc, c5!=cc, c6!=cc, c7!=cc);
        }
        
        // horizontal
        if(is(cc, [c5,c6,c3,c4,c0], [c7])) return [8,12];
        if(is(cc, [c1,c2,c3,c4,c7], [c0])) return [10,14];
        if(is(cc, [c1,c2], [c5,c6])) return [16,20];
        if(is(cc, [c5,c6], [c1,c2])) return [18,22];
        
        // vertical
        if(is(cc, [c2,c6], [c1,c5])) return [17,21];
        if(is(cc, [c1,c5], [c2,c6])) return [19,23];
        
        // corner inner
        if(is(cc, [c1,c5,c0,c7], [c3])) return [9,13];
        if(is(cc, [c2,c6,c0,c7], [c4])) return [11,15];
        
        // corner outer
        if(is(cc, [c2,c6,c4], [c0,c5])) return [17,21];
        if(is(cc, [c2,c6,c4], [c0,c7])) return [17,21];
        if(is(cc, [c1,c5,c3], [c0,c6])) return [19,23];
        if(is(cc, [c1,c5,c3], [c0,c7])) return [19,23];
        
        // diagonal
        if(is(cc, [c5,c2], [c6])) return [0,4];
        if(is(cc, [c5,c2], [c4,c7])) return [0,4];
        if(is(cc, [c1,c6], [c5])) return [1,5];
        if(is(cc, [c1,c6], [c3,c7])) return [1,5];
        if(is(cc, [c5,c2], [c1])) return [2,6];
        if(is(cc, [c5,c2], [c3,c0])) return [2,6];
        if(is(cc, [c1,c6], [c2])) return [3,7];
        if(is(cc, [c1,c6], [c0,c4])) return [3,7];
        
        return [23];
    }
    
    /*
     *                             -- even                          -- odd
     *       c0                    +0.-2                            +0.-2  
     *    c1    c2           -1.-1       +0.-1                +0.-1       +1.-1   
     * c3    cc    c4  -1.+0       +0.+0       +1.+0    -1.+0       +0.+0       +1.+0
     *    c5    c6           -1.+1       +0.+1                +0.+1       +1.+1  
     *       c7                    +0.+2                            +0.+2 
     */
    _vis.terrainTileMapper = function(cc, c0, c1, c2, c3, c4, c5, c6, c7) {
        var d;
        switch (cc) {
            case '_': d=[{setname: 'cave', tilename: 'bones', variation:[0], z: 0}]; break;
            case 'G': {
                // water on a nightbour
                if (!is('W', false, [c0, c1, c2, c3, c4, c5, c6, c7])) {
                      d=[{setname: 'grassland', tilename: 'watercliff', variation:_vis.tileVariationForWall('W', c0, c1, c2, c3, c4, c5, c6, c7, true), z: 0}];
                } else {
                      d=[{setname: 'grassland', tilename: 'grass', variation:'all', z: 0}];
                }
                break;
            }
            case 'P': d=[{setname: 'grassland', tilename: 'path', variation:'all', z: 0}]; break;
            case 'B': d=[{setname: 'cave', tilename: 'bones', variation:'all', z: 0}]; break;
            case 'S': {
                if (is(cc, [c0, c1, c2, c3, c4, c5, c6, c7])) {
                      d=[{setname: 'grassland', tilename: 'grass', variation:'all', z: 2}]; break;
                }
                if (is(cc, [c0,c1,c2]) || is(cc, [c2,c4,c6]) || is(cc, [c5,c6,c7]) || is(cc, [c1,c3,c5])) {
                      d=[{setname: 'grassland', tilename: 'grass', variation:'all', z: 0},
                         {setname: 'grassland', tilename: 'cliff', variation:_vis.tileVariationForWall(cc, c0, c1, c2, c3, c4, c5, c6, c7), z: 0}];
                } else {
                      d=[{setname: 'grassland', tilename: 'grass', variation:'all', z: 0},
                         {setname: 'grassland', tilename: 'rock', variation:'all', z: 0}];
                }
                break;
            }
            case 'W': {
                      d=[{setname: 'grassland', tilename: 'water', variation:'all', z: -1}]; break;
            }
        }
        return d;
    }
    
    _vis.objectTileMapper = function(cc) {
        var d
        
        switch(cc) {
            case '_': d = false; break;
            case 'T': d = [{setname: 'grassland', tilename: 'oak', variation:'all', z: 0, x: -0.5}]; break;
        }
        
        return d
    }
}
