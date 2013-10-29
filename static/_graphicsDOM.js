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

_graphicsDOM = new function() { var _graphics = this;
  var TILE_XS
  var TILE_YS
  var TILE_XS_HALF
  var TILE_YS_HALF
  var VIEW_XS
  var VIEW_YS
  var CHUNK_SIZE = _.CHUNK_SIZE;
  
  /* number of chucks which stay in the view messured from the chuck the player
   * is in.
   * number_of_chunks_loaded = (VIEW_CHUNKSBUFFER_X*2+1) * (VIEW_CHUNKSBUFFER_Y*2+1) */
  var VIEW_CHUNKSBUFFER_X = 2
  var VIEW_CHUNKSBUFFER_Y = 4
  
  /* viewport chunk position offset, messured in chunks */
  var cxo = 0
  var cyo = 0
  
  /*
   * logging
   */
  var log = new function() {};
  log.error = function(msg) {console.error(msg)}
  log.info = function(msg) {console.log(msg)}
  
  /*
   * randomizing
   */
  var Random = function(seed) {
    /* https://gist.github.com/banksean/300494 */
    return new MersenneTwister(seed)
  }
  
  _graphics.init = function(tile_xs, tile_ys, terrainTileMapper, objectTileMapper) {
    TILE_XS = tile_xs;
    TILE_XS_HALF = TILE_XS / 2;
    TILE_YS = tile_ys;
    TILE_YS_HALF = TILE_YS / 2;
    
    _graphics.initCss();
    _graphics.setTerrainTileMapper(terrainTileMapper);
    _graphics.setObjectTileMapper(objectTileMapper);
  }

  _graphics.initWindow = function(windowhandler, xs, ys) {
    VIEW_XS = xs;
    VIEW_YS = ys;
    windowhandler.width(VIEW_XS).height(VIEW_YS)
      .addClass('_renderingWindowDOM');
    _graphics.map = [];
    _graphics.renderedChunks = {};
    _graphics.viewport = windowhandler;
    _graphics.initChunkContainers()
  }
  
  _graphics.initCss = function() {
    /* add some global css */
    var stylesheet = document.styleSheets[0];
    var css = function(selector, rule) {
      if (stylesheet.insertRule) {
        stylesheet.insertRule(selector + rule, stylesheet.cssRules.length);
      } else if (stylesheet.addRule) {
        stylesheet.addRule(selector, rule, -1);
      }
    }
    // rendering window
    css('._renderingWindowDOM', '{background-color: white; position: relative; overflow: auto;}');
    // tile properties
    css('._renderingWindowDOM .chunkcontainer', '{position: absolute; background-color:red;}');
    css('._renderingWindowDOM .chunk', '{position: absolute;}');
    css('._renderingWindowDOM .tile', '{position: absolute; display: table;opacity : 1.0;}');
    css('._renderingWindowDOM .tilepart', '{position: absolute; display: table;opacity : 1.0;}');
    css('._renderingWindowDOM .tile p', '{display: table-cell; vertical-align: middle; text-align: center;font-size: 10px; opacity : 1.0;}');
  }
  
  _graphics.createTile = function(tiledata, i, j, randomValue) {
    var multitile = $('<div></div>').addClass('tile');
    multitile.css({
      'width': (TILE_XS) + 'px',
      'height': (TILE_YS) + 'px'
    });
    for (var key in tiledata) {
      var tile = createTilePart(tiledata[key], i, j, randomValue);
      multitile.append(tile);
    }
    
    //var content = $('<p>'+i+'.'+j+'</p>');
    //multitile.append(content);
    
    return multitile;
  }
  var createTilePart = function(tiledata, i, j, randomValue) {
    var tileset = _.tileset(tiledata.setname);
    var tile = _.tile(tiledata.setname, tiledata.tilename);
    var variation
    if (!tiledata.variation) {
      variation = 0;
    }
    else if (tiledata.variation == 'all') {
      variation = Math.floor(randomValue * tile.length);
    }
    else if (tiledata.variation.length > 0) {
      variation = tiledata.variation[Math.floor(randomValue * tiledata.variation.length)];
    }
    else {
      variation = tiledata.variation;
    }
    
    var ox = tile[variation].x;
    var oy = tile[variation].y;
    
    var margintop = (TILE_YS * (tile.ys - 1 - tile.origin) + (TILE_YS*tiledata.z)) * -1;
    var marginleft = tiledata.x ? (TILE_XS * tiledata.x) : 0;
    var t = $('<div></div>').addClass('tilepart').css({
      'width': (TILE_XS * tile.xs) + 'px',
      'height': (TILE_YS * tile.ys) + 'px',
      'margin-top': margintop + 'px',
      'margin-left': marginleft + 'px',
      //'background-color': colors[Math.round(Math.random(colors.length))], 
      'background-image': 'url("' + tileset.url + '")',
      'background-position': '-'+ox+'px -'+oy+'px',
      //'background-repeat': 'no-repeat',
      //'background-position': 'center center'
    }).attr('z', tiledata.z);
    
    return t;
  }
  
  //_graphics.viewportRectCalc = function(x, y) {
  //    return {
  //        i1Even: Math.round((x) / TILE_YS) - 1,
  //        i2Even: Math.round((x + VIEW_XS) / TILE_XS),
  //        i1Odd:  Math.round((x - TILE_XS_HALF) / TILE_YS) - 1,
  //        i2Odd:  Math.round((x + TILE_XS_HALF + VIEW_XS) / TILE_XS),
  //        j1:     Math.ceil((y) / TILE_YS_HALF) - 1,
  //        j2:     Math.ceil((y + VIEW_YS) / TILE_YS_HALF) + 1
  //    };
  //}
  
  /*
   * chunks
   */
  _graphics.chunk = function(cx, cy) {
    var lookupIdx = (cx + '.' + cy);
    var chunk = _graphics.renderedChunks[lookupIdx];
    if (!chunk) {
      chunk = $('<div></div>').addClass('chunk');
      chunk.cx = cx
      chunk.cy = cy
      _graphics.renderedChunks[lookupIdx] = chunk
    }
    return chunk;
  }
  /* create chunk position placeholders */
  _graphics.initChunkContainers = function() {
    _graphics.viewport.chunkContainers = {}
    for (var y = 0; y < VIEW_CHUNKSBUFFER_Y*2+1; y++) {
      for (var x = 0; x < VIEW_CHUNKSBUFFER_X*2+1; x++) {
        var chunkContainer = $('<div></div>').addClass('chunkcontainer');
        chunkContainer.css({  
          'left': (x * CHUNK_SIZE * TILE_XS) + 'px',
          'top':  (y * CHUNK_SIZE * TILE_YS_HALF) + 'px',
          'width':   (CHUNK_SIZE * TILE_XS) + 'px',
          'height':  (CHUNK_SIZE * TILE_YS_HALF) + 'px',
        });
        
        var lookupIdx = (x + '.' + y)
        _graphics.viewport.chunkContainers[lookupIdx] = chunkContainer
        _graphics.viewport.append(chunkContainer);
      }
    }
  }
  /* set the position of the chunk (div) in the viewport */
  var alignChunkInViewport = function(chunkElem) {
    chunkElem.remove()
    
    var cxr = chunkElem.cx - cxo
    var cyr = chunkElem.cy - cyo
    var lookupIdx = (cxr + '.' + cyr)
    var chunkContainer = _graphics.viewport.chunkContainers[lookupIdx]
    
    if(!chunkContainer) {
      // garbage collecting old unused chunks
      var lookupIdx = (chunkElem.cx + '.' + chunkElem.cy)
      delete _graphics.renderedChunks[lookupIdx]
      return
    }
    chunkContainer.empty()
    chunkContainer.append(chunkElem)
  }
  
  _graphics.isChunkRendered = function(cx, cy) {
    var lookupIdx = (cx + '.' + cy);
    return !!_graphics.renderedChunks[lookupIdx];
  }
  _graphics.isChunkInViewport = function(cx, cy) {
    if(cx < cxo || cx > cxo + VIEW_CHUNKSBUFFER_X*2+1)
      return false
    if(cy < cyo || cy > cyo + VIEW_CHUNKSBUFFER_Y*2+1)
      return false
    return true
  }
  _graphics.renderChunk = function(cx, cy, updateOnly) {
    if (!_graphics.isChunkInViewport(cx, cy)) return;
    _.scheduler.enqueue(function() {_graphics.renderChunk0(cx,cy,updateOnly)})
  }
  _graphics.renderChunk0 = function(cx, cy, updateOnly) {
    if ( !_graphics.isChunkInViewport(cx, cy)
      || updateOnly && !_graphics.isChunkRendered(cx, cy)) {
      _.scheduler.next()
      return;
    }
    
    var chunkElem = _graphics.chunk(cx, cy);
    /* remove the element from the dom to prevent successiv updates */
    chunkElem.remove()
    /* delete old tiles, optimize this later */
    chunkElem.empty()
    
    /* deterministic 'pseudo'-random generator.
     * The generated numbers has to be only depend on the chuck which is rendered
     * to ensure that successive rendering of the same chunk produces the the
     * same result. */
    rnd = Random(cy * CHUNK_SIZE + cx)
    
    /* prepare terrain rendering */
    var terrain = _.chunkBordered(cx, cy).view('terrain')
    /* prepate object rendering */
    var objects = _.chunk        (cx, cy).view('objects')
    
    for (var j = 0; j < CHUNK_SIZE; j++) {
      var ioffset = j%2 ? TILE_XS_HALF : 0
      var ay = j + cy * CHUNK_SIZE;
      var tile_y = (j * TILE_YS_HALF);
      for (var i = 0; i < CHUNK_SIZE; i++) {
        var ax = i + cx * CHUNK_SIZE;
        var tile_x = (i * TILE_XS) + ioffset;
        /* pick one 'pseudo'-random value for each cell of the chunk, the order
         * of iteration has to be the same whenever generating the same chunk
         * to ensure to get the same 'pseudo'-random value for each cell */
        var randomValue = rnd.random()
        //var randomValue = 0;
        
        /* render terrain */
        {
          /*
           *                             -- even                          -- odd
           *       c0                    +0.-2                            +0.-2  
           *    c1    c2           -1.-1       +0.-1                +0.-1       +1.-1   
           * c3    cc    c4  -1.+0       +0.+0       +1.+0    -1.+0       +0.+0       +1.+0
           *    c5    c6           -1.+1       +0.+1                +0.+1       +1.+1  
           *       c7                    +0.+2                            +0.+2 
           */ 
          var o = ay%2 ? 1 : 0;
          var tile = _graphics.terrainTileMapper(
            terrain.get(i    , j  ), // cc
            terrain.get(i+0  , j-2), // c0
            terrain.get(i-1+o, j-1), terrain.get(i+0+o, j-1), // c1, c2
            terrain.get(i-1  , j+0), terrain.get(i+1  , j+0), // c3, c4
            terrain.get(i-1+o, j+1), terrain.get(i+0+o, j+1), // c5, c6
            terrain.get(i+0  , j+2)  // c7
          )
          if(tile) {
            var tileElem = _graphics.createTile(tile, ax, ay, randomValue)
            tileElem.css({  
              'left': tile_x + 'px',
              'top':  tile_y + 'px'
            });
            tileElem.children('.tilepart').each(function() {
              var zoffset = parseInt($(this).attr('z')); if (!zoffset) zoffset = 0;
              $(this).css({
                'z-index': (ay + zoffset)  
              });
            });
            chunkElem.append(tileElem);
          }
        }
        /* render objects */
        {
          var tile = _graphics.objectTileMapper(objects.get(i,j))
          if(tile) {
            var tileElem = _graphics.createTile(tile, ax, ay, randomValue)
            tileElem.css({  
              'left': tile_x + 'px',
              'top':  tile_y + 'px'
            });
            tileElem.children('.tilepart').each(function() {
              var zoffset = parseInt($(this).attr('z')); if (!zoffset) zoffset = 0;
              $(this).css({
                'z-index': (ay + zoffset + 1)   // rem this +1 asap
              });
            });
            chunkElem.append(tileElem);
          }
        }
      }
    }
    alignChunkInViewport(chunkElem)
  }
  
  _graphics.setTerrainTileMapper = function(terrainTileMapper) {
    _graphics.terrainTileMapper = terrainTileMapper;
  }
  _graphics.setObjectTileMapper = function(objectTileMapper) {
    _graphics.objectTileMapper = objectTileMapper;
  }
  
  _graphics.centerCell = function(x,y) {
    var cx = Math.floor(x / CHUNK_SIZE)
    var cy = Math.floor(y / CHUNK_SIZE)
    var view_cx0 = cx - VIEW_CHUNKSBUFFER_X
    var view_cy0 = cy - VIEW_CHUNKSBUFFER_Y
    
    /* realign viewport */
    if(view_cx0 != cxo || view_cy0 != cyo) {    
      //log.info('move view to ul corner to: '+ view_cx0 + ':' + view_cy0)
      cxo = view_cx0
      cyo = view_cy0
      
      _graphics.renderViewport()
    }
    
    // relative position in the view
    var rx = x - cxo * CHUNK_SIZE
    var ry = y - cyo * CHUNK_SIZE
    
    _graphics.viewport
      //           tileoffset          viewcenter  tilecenter     y-odd rows are offseted by TILE_XS_HALF
      .scrollLeft( rx * TILE_XS      - VIEW_XS/2 + TILE_XS_HALF + (ry%2==0 ? 0 : TILE_XS_HALF) )
      .scrollTop ( ry * TILE_YS_HALF - VIEW_YS/2 + TILE_YS_HALF )
  }
  
  _graphics.renderViewport = function() {
    for(var j = 0; j < VIEW_CHUNKSBUFFER_Y*2; j++) {
      for(var i = 0; i < VIEW_CHUNKSBUFFER_X*2; i++) {
        var cx = i + cxo;
        var cy = j + cyo;
        
        if(_graphics.isChunkRendered(cx,cy)) {
          var lookupIdx = (cx + '.' + cy);
          var chunk = _graphics.renderedChunks[lookupIdx];
          alignChunkInViewport(chunk)
        }
        else {
          _graphics.renderChunk(cx, cy)
        }
      }
    }
  }
}

/* OLD */
//_graphics.renderChunk0 = function(cx, cy, updateOnly) {
//    if (updateOnly && !_graphics.isChunkCached(cx, cy)) return;
//    
//    var chunk = _graphics.chunk(cx, cy);
//    for (var j = 0; j < CHUNK_SIZE; j++) {
//        if (j % 2) {
//            var ioffset = TILE_XS_HALF;
//        }
//        else {
//            var ioffset = 0;
//        }
//        
//        var ay = j + cy * CHUNK_SIZE;
//        var tile_y = (j * TILE_YS_HALF);
//        for (var i = 0; i < CHUNK_SIZE; i++) {
//            var ax = i + cx * CHUNK_SIZE;
//            var tile_x = (i * TILE_XS) + ioffset;
//            var lookupIdx = (i + '.' + j);
//            /* detelet old tile and force lookup miss, optimize this later */
//            if (chunk.terrain[lookupIdx]) {
//                chunk.terrain[lookupIdx].remove();
//                delete chunk.terrain[lookupIdx];
//            }
//            /* tile lookup miss */
//            if (!chunk.terrain[lookupIdx]) {
//                var tile = _graphics.createTile(chunk.data.terrain[lookupIdx], ax, ay);
//                tile.css({  
//                    'left': tile_x + 'px',
//                    'top':  tile_y + 'px'
//                });
//                tile.children('.tilepart').each(function() {
//                    var zoffset = parseInt($(this).attr('z')); if (!zoffset) zoffset = 0;
//                    $(this).css({
//                        'z-index': (ay + zoffset)  
//                    });
//                });
//                chunk.terrain[lookupIdx] = tile;
//                chunk.append(tile);
//            }
//            
//            /* objects */
//            //var object = _graphics.createObject(chunk.data.objects[lookupIdx])
//            //object.css({  
//            //    'left': tile_x + 'px',
//            //    'top':  tile_y + 'px',
//            //    'z-index': ay
//            //});
//            //chunk.append(object)
//        }
//    }
//    alignChunkInViewport(chunk)
//}


//_graphics.generateChunkTilemap = function(cx, cy) {
//    var cs = {
//        '-1.-1' : _.chunk(cx-1, cy-1),
//        '0.-1'  : _.chunk(cx  , cy-1),
//        '1.-1'  : _.chunk(cx+1, cy-1),
//        '-1.0'  : _.chunk(cx-1, cy  ),
//        '0.0'   : _.chunk(cx  , cy  ),
//        '1.0'   : _.chunk(cx+1, cy  ),
//        '-1.1'  : _.chunk(cx-1, cy+1),
//        '0.1'   : _.chunk(cx  , cy+1),
//        '1.1'   : _.chunk(cx+1, cy+1)
//    }
//    
//    var get = function(x,y) {
//        var ox = Math.floor(x / CHUNK_SIZE) // chunk offset x
//        var oy = Math.floor(y / CHUNK_SIZE) // chunk offset y
//        var mx = x % CHUNK_SIZE;            // chunk index x
//        mx = mx < 0 ? CHUNK_SIZE + mx : mx; // correct negative %
//        var my = y % CHUNK_SIZE;            // chunk index y
//        my = my < 0 ? CHUNK_SIZE + my : my; // correct negative %
//        
//        return cs[ox + '.' + oy].data.terrain[(mx) + CHUNK_SIZE*(my)];
//    }
//                        
//    var terrain = [];
//    for (var j = 0; j < CHUNK_SIZE; j++) {
//        for (var i = 0; i < CHUNK_SIZE; i++) {  
//            var lookupIdx = (i + '.' + j);
//            /*
//             *                             -- even                          -- odd
//             *       c0                    +0.-2                            +0.-2  
//             *    c1    c2           -1.-1       +0.-1                +0.-1       +1.-1   
//             * c3    cc    c4  -1.+0       +0.+0       +1.+0    -1.+0       +0.+0       +1.+0
//             *    c5    c6           -1.+1       +0.+1                +0.+1       +1.+1  
//             *       c7                    +0.+2                            +0.+2 
//             */
//            if (j % 2 == 0) {
//                terrain[lookupIdx] = _graphics.tilemapper(
//                    get(i  , j  ), // cc
//                    get(i+0, j-2), // c0
//                    get(i-1, j-1), // c1
//                    get(i+0, j-1), // c2
//                    get(i-1, j+0), // c3
//                    get(i+1, j+0), // c4
//                    get(i-1, j+1), // c5
//                    get(i+0, j+1), // c6
//                    get(i+0, j+2)  // c7
//                )
//            }
//            else {
//                terrain[lookupIdx] = _graphics.tilemapper(
//                    get(i  , j  ), // cc
//                    get(i+0, j-2), // c0
//                    get(i+0, j-1), // c1
//                    get(i+1, j-1), // c2
//                    get(i-1, j+0), // c3
//                    get(i+1, j+0), // c4
//                    get(i+0, j+1), // c5
//                    get(i+1, j+1), // c6
//                    get(i+0, j+2)  // c7
//                )
//            }
//        }
//    }
//    return terrain;
//}
//_graphics.generateObjectTiles = function(cx, cy) {
//    c = _.chunk(cx, cy)
//    var objects = []
//    for (var j = 0; j < CHUNK_SIZE; j++) {
//        for (var i = 0; i < CHUNK_SIZE; i++) {
//            var lookupIdx = (i + '.' + j)
//            var object = c.data.objects[lookupIdx]
//            objects[lookupIdx] = _graphics.tilemapper.object(object)
//        }
//    }
//    return objects
//}
