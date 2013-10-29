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

_graphicsASCII = new function() { var _graphics = this;
  var TILE_XS = 24;
  var TILE_YS = 24;
  var TILE_XS_HALF
  var TILE_YS_HALF
  var VIEW_XS
  var VIEW_YS
  var CHUNK_SIZE = _.CHUNK_SIZE;
  
  /*
   * logging
   */
  var log = new function() {};
  log.error = function(msg) {console.error(msg)}
  log.info = function(msg) {console.log(msg)}
  
  _graphics.init = function() {
    TILE_XS_HALF = TILE_XS / 2;
    TILE_YS_HALF = TILE_YS / 2;
    
    _graphics.initCss();
  }

  _graphics.initWindow = function(windowhandler, xs, ys) {
    VIEW_XS = xs;
    VIEW_YS = ys;
    windowhandler.width(VIEW_XS).height(VIEW_YS)
      .addClass('_renderingWindowASCII');
    _graphics.map = [];
    _graphics.chunks = [];
    _graphics.viewport = windowhandler;
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
    css('._renderingWindowASCII', '{background-color: white; position: relative; overflow: auto;}');
    // tile properties
    css('._renderingWindowASCII .chunk', '{position: absolute; box-shadow: 0px 0px 2px #888;}');
    css('._renderingWindowASCII .tile', '{position: absolute; display: table;opacity : 1.0;}');
    css('._renderingWindowASCII .input', '{margin-left: 2px; border: 0; font-size: 10px; font-family: monospace; letter-spacing: 5px; width: '+(TILE_XS*CHUNK_SIZE-4)+'px;}');
  }
  
  /*
   * chunks
   */
  
  _graphics.chunk = function(cx, cy) {
    var lookupIdx = (cx + '.' + cy);
    var chunk = _graphics.chunks[lookupIdx];
    if (!chunk) {
      chunk = $('<div></div>').addClass('chunk');
      chunk.css({  
        'left': (cx * CHUNK_SIZE * TILE_XS) + 'px',
        'top':  (cy * CHUNK_SIZE * TILE_YS) + 'px',
        'width': (CHUNK_SIZE * TILE_XS) + 'px',
        'height':  (CHUNK_SIZE * TILE_YS) + 'px',
      });
      chunk.terrain = [];
      
      chunk.append($('<h4>'+cx+'.'+cy+'</h4>'));
      chunk.append($('<input type="submit" value="refresh"/>'));
      
      // linewise inputs
      for (var y = 0; y < CHUNK_SIZE; y++) {
        chunk.append($('<input type="text" name="'+y+'" value="">').addClass('input'));
      }
      _graphics.chunks[lookupIdx] = chunk;
      _graphics.viewport.append(chunk);
    }
    chunk.data = {
      terrain : _graphics.generateChunkTilemap(cx, cy)
    }
    return chunk;
  }
  
  _graphics.isChunkCached = function(cx, cy) {
    var lookupIdx = (cx + '.' + cy);
    return !!_graphics.chunks[lookupIdx];
  }
  
  _graphics.renderChunk = function(cx, cy, updateOnly) {
    if (updateOnly && !_graphics.isChunkCached(cx, cy)) return;
    
    var chunk = _graphics.chunk(cx, cy);
    
    /* delete old content, optimize this later */
    chunk.remove('.input');
    
    for (var j = 0; j < CHUNK_SIZE; j++) {
      if (j % 2) {
        var line = ' ';
      }
      else {
        var line = ''
      }
      
      for (var i = 0; i < CHUNK_SIZE; i++)
      {
        var lookupIdx = (i + '.' + j);
        line = line + chunk.data.terrain[lookupIdx] + ' ';
      }
      chunk.children('[name="' + j + '"]').attr('value', line);
      //chunk.append($('<input type="text" name="'+j+'" value="'+line+'">').addClass('input'));
    }
  }
  
  _graphics.generateChunkTilemap = function(cx, cy) {
    var c = _.chunk(cx, cy);  
    var terrain = [];
    for (var j = 0; j < CHUNK_SIZE; j++) {
      for (var i = 0; i < CHUNK_SIZE; i++) {
        var lookupIdx = (i + '.' + j);
        terrain[lookupIdx] = c.data.terrain[i + CHUNK_SIZE*j];
      }
    }
    return terrain;
  }
  
  _graphics.centerCell = function(x,y) {
    
  }
}
