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
    
    var isPositive = function(vs) {
        return ands(vs, function (v) {return v >= 0})
    }
    
    var isGreater2 = function(vs) {
        return ors(vs, function (v) {return v >= 2})
    }
    
    var ands = function(vs, f) {
    	for (var key in vs) {
            if(!f(vs[key])) return false
        }
        return true;
    }
    
    var ors = function(vs, f) {
    	for (var key in vs) {
            if(f(vs[key])) return true
        }
        return false;
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
    
    _vis.tileVariationForWall_Format_ = function(cc, c0, c1, c2, c3, c4, c5, c6, c7, swap) {
        if (swap) {
            return _vis.tileVariationForWall_Format_(true, c0!=cc, c1!=cc, c2!=cc, c3!=cc, c4!=cc, c5!=cc, c6!=cc, c7!=cc);
        }
        
        // horizontal
        if(is(cc, [c5,c6,c3,c4,c0], [c7])) return [4];
        if(is(cc, [c1,c2,c3,c4,c7], [c0])) return [6];
        if(is(cc, [c1,c2], [c5,c6])) return [8];
        if(is(cc, [c5,c6], [c1,c2])) return [10];
        
        // vertical
        if(is(cc, [c2,c6], [c1,c5])) return [9];
        if(is(cc, [c1,c5], [c2,c6])) return [11];
        
        // corner inner
        if(is(cc, [c1,c5,c0,c7], [c3])) return [5];
        if(is(cc, [c2,c6,c0,c7], [c4])) return [7];
        
        // corner outer
        if(is(cc, [c2,c6,c4], [c0,c5])) return [9];
        if(is(cc, [c2,c6,c4], [c0,c7])) return [9];
        if(is(cc, [c1,c5,c3], [c0,c6])) return [11];
        if(is(cc, [c1,c5,c3], [c0,c7])) return [11];
        
        // diagonal
        if(is(cc, [c5,c2], [c6])) return [0];
        if(is(cc, [c5,c2], [c4,c7])) return [0];
        if(is(cc, [c1,c6], [c5])) return [1];
        if(is(cc, [c1,c6], [c3,c7])) return [1];
        if(is(cc, [c5,c2], [c1])) return [2];
        if(is(cc, [c5,c2], [c3,c0])) return [2];
        if(is(cc, [c1,c6], [c2])) return [3];
        if(is(cc, [c1,c6], [c0,c4])) return [3];
        
        return [0];
    }
    
    _vis.tileVariationForRamp_Format = function(cc, c0, c1, c2, c3, c4, c5, c6, c7, swap) {
        return _vis.tileVariationForWall_Format_(true, cc<=c0, cc<=c1, cc<=c2, cc<=c3, cc<=c4, cc<=c5, cc<=c6, cc<=c7, false);
    }
    
    /*
     *       c0         
     *    c1    c2      
     * c3    cc    c4 
     *    c5    c6    
     *       c7      
     */
    _vis.terrainTileMapper = function(
      cc, // center ground
      c0, c1, c2, c3, c4, c5, c6, c7, // neighbor ground
      h0, h1, h2, h3, h4, h5, h6, h7  // neighbor height
    ) {
        var d;
        switch (cc) {
            case '_': d=[{setname: 'cave', tilename: 'bones', variation:[0], z: 0}]; break;
            case 'G': {
                // water on a nightbour
                if (!is('W', false, [c0, c1, c2, c3, c4, c5, c6, c7])) {
                      d=[{setname: 'terrain_grass', tilename: 'water', variation:'all', z: -1},
                         {setname: 'terrain_grass', tilename: 'cliff1', variation:_vis.tileVariationForWall_Format_('W', c0, c1, c2, c3, c4, c5, c6, c7, true), z: -1}];
                } else if (is(0, [h0, h1, h2, h3, h4, h5, h6, h7])) {
                	  d=[{setname: 'terrain_grass', tilename: 'floor', variation:'all', z: 0}];
                } else if (isPositive([h0, h1, h2, h3, h4, h5, h6, h7])) {
                	  d=[{setname: 'terrain_grass', tilename: 'floor', variation:'all', z: 0}];
                } else if (isGreater2([-h1, -h2, -h5, -h6])){
            	      d=[{setname: 'terrain_grass', tilename: 'floor', variation:'all', z: -1},
                         {setname: 'terrain_grass', tilename: 'cliff1', variation:_vis.tileVariationForRamp_Format(0, h0, h1, h2, h3, h4, h5, h6, h7), z: -1}];
                } else {
                      d=[{setname: 'terrain_grass', tilename: 'floor', variation:'all', z: -0.5},
                         {setname: 'terrain_grass', tilename: 'ramp', variation:_vis.tileVariationForRamp_Format(0, h0, h1, h2, h3, h4, h5, h6, h7), z: -0.5}];
                }
                break;
            }
            case 'P': d=[{setname: 'grassland', tilename: 'path', variation:'all', z: 0}]; break;
            case 'B': d=[{setname: 'cave', tilename: 'bones', variation:'all', z: 0}]; break;
            case 'S': {
                if (is(cc, [c0, c1, c2, c3, c4, c5, c6, c7])) {
                      d=[{setname: 'terrain_grass', tilename: 'floor', variation:'all', z: 2}]; break;
                }
                if (is(cc, [c0,c1,c2]) || is(cc, [c2,c4,c6]) || is(cc, [c5,c6,c7]) || is(cc, [c1,c3,c5])) {
                      d=[{setname: 'terrain_grass', tilename: 'floor', variation:'all', z: 0},
                         {setname: 'terrain_grass', tilename: 'cliff2', variation:_vis.tileVariationForWall_Format_(cc, c0, c1, c2, c3, c4, c5, c6, c7), z: 0}];
                } else {
                      d=[{setname: 'terrain_grass', tilename: 'floor', variation:'all', z: 0},
                         {setname: 'grassland', tilename: 'rock', variation:'all', z: 0}];
                }
                break;
            }
            case 'W': {
                      d=[{setname: 'terrain_grass', tilename: 'water', variation:'all', z: -1}]; break;
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
