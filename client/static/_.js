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

_ = new function() { var _ = this;
    var CHUNK_SIZE = 8;

    _.TILESET_DIR = 'static/tiles/';
    _.CHUNK_SIZE = CHUNK_SIZE;
    _.CHUNK_MISS = {
        data : {
            terrain: Array(CHUNK_SIZE*CHUNK_SIZE+1).join('_'), // see: http://stackoverflow.com/questions/1877475/repeat-character-n-times
            objects: Array(CHUNK_SIZE*CHUNK_SIZE+1).join('_'),
        },
        view : function(name) {
            return new ChunkView(this.data[name])
        }
    };

    /*
     * logging
     */
    var logger = new function() {};
    logger.error = function(msg) {console.error(msg)}
    logger.info = function(msg) {return; console.log(msg)}

    _.start = function() {
        _.connect()
        _.bindControls()
    }
    _.connect = function() {
        /*
         * socket handling
         */
        var socket = new WebSocket("ws://localhost:10000/");
        var isopen = false
        
        // What do we do when we get a message?
        socket.onmessage = function(evt) {
            logger.info('#in: ' + evt.data);
            var msg = JSON.parse(evt.data);
            if (!msg.type) {
                logger.error('socket message "type" not set on message "' + evt.data + '"');
                return;
            }
            if (!(msg.type in _.msgHandler)) {
                logger.error('engine message handler does not support message type "' + msg.type +'"');
                return;
            }
            _.msgHandler[msg.type](msg.data);
        }
        
        // Just update our conn_status field with the connection status
        socket.onopen = function(evt) {
            isopen = true
            $('#_conn #_conn_status').html('<b>Connected</b>');
        }
        socket.onerror = function(evt) {
            $('#_conn #_conn_status').html('<b>Error</b>');
        }
        socket.onclose = function(evt) {
            isopen = false
            $('#_conn #_conn_status').html('<b>Closed</b>');
        }
        
        _.sendMessage = function(msgtype, data) {
            if(!isopen) {
                logger.info('socket not open')
                return
            }
            jsonMsg = JSON.stringify({type: msgtype, data: data})
            socket.send(jsonMsg)
        }
    }
    
    /*
     * chunks
     */
    _.chunks = [];
    /* Updates the chunkdata of chunk(cx,cy) if any are given (chunkdata parameter is set),
     * otherwise the chunk(cx,cy) is returned. */
    _.chunk = function(cx, cy, chunkdata) {
        var lookupIdx = (cx + '.' + cy);
        var chunk = _.chunks[lookupIdx];
        
        if (chunkdata) {
            if (!chunk) {
                chunk = {}
                chunk.view = function(name) {
                    return new ChunkView(this.data[name])
                }
                _.chunks[lookupIdx] = chunk;
            }
            chunk.data = chunkdata;
        }
        else {
            if (!chunk) {
                //logger.error('chunk miss ' + cx + '.' + cy + '');
                return _.CHUNK_MISS;
            }
        }	
        return chunk;
    }
    /* A view on only one data-array of a chunk */
    var ChunkView = function(data) {
        this.data = data
    }
    ChunkView.prototype.get = function(x, y) {
        return this.data[y * CHUNK_SIZE + x]
    }
    /* A smart access method to a chunk with all its 8 neighbor chunks. */
    _.chunkBordered = function(cx, cy) {
        var chunkBordered = {}
        chunkBordered.view = function(name) {
            return new ChunkBorderedView(cx, cy, name)
        }
        return chunkBordered
    }
    /* A view on only one data-array of a bordered-chunk */
    var ChunkBorderedView = function(cx, cy, name) {
        var g = function(cx, cy) {return _.chunk(cx, cy).view(name)}
        this.data = [
            g(cx-1,cy-1), g(cx  ,cy-1), g(cx+1,cy-1),
            g(cx-1,cy  ), g(cx  ,cy  ), g(cx+1,cy  ),
            g(cx-1,cy+1), g(cx  ,cy+1), g(cx+1,cy+1)
        ]
    }
    ChunkBorderedView.prototype.get = function(x, y) {
        x += CHUNK_SIZE; y += CHUNK_SIZE;
        var cx = Math.floor(x / CHUNK_SIZE)
        var cy = Math.floor(y / CHUNK_SIZE)
        var mx = x % CHUNK_SIZE
        var my = y % CHUNK_SIZE
        return this.data[cy * 3 + cx].get(mx, my)
    }
    
    /*
     * tilesets
     */
    _.tileset = function(setname) {
        return _.tileset[setname];
    }
    _.tile = function(setname, tilename) {
        var tileset = _.tileset[setname];
        if (!tileset) {
            logger.error('no tileset "' + setname + '"');
        }
        var tile = tileset[tilename];
        if (!tile) {
            logger.error('no tile "' + tilename + '" in set "' + setname + '"');
        }
        return tile;
    }
    
    /*
     * graphic adapter
     */
    _.graphics = [];
    _.createRenderingWindow = function(graphicsImpl, windowselector, xs, ys) {
        _.graphics[windowselector] = graphicsImpl;
        graphicsImpl.initWindow($(windowselector), xs, ys);
    }
    _.centerCell = function(x,y) {
        for (var key in _.graphics) {
            g = _.graphics[key]
            g.centerCell(x,y)
        }
    }
    
    /*
     * message handler
     */
    _.msgHandler = [];
    _.addMessageHandler = function(msgtype, handler) {
        _.msgHandler[msgtype] = handler
    }
    
    _.addMessageHandler('chunk', function(msg) {
        var cx = parseInt(msg.cx)
        var cy = parseInt(msg.cy)
        logger.info(msg.chunkdata);
        _.chunk(cx, cy, msg.chunkdata);
        for (var key in _.graphics) {
            g = _.graphics[key]
            g.renderChunk(cx+0, cy+0);
        }
    });
    
    _.addMessageHandler('move_position', function(msg) {
        var x = parseInt(msg.x)
        var y = parseInt(msg.y)
        _.centerCell(x,y)
    });
    
    /* player and location */
    _.move = function(direction) {
        _.sendMessage('move_delta', direction)
    }
    /* key handler */
    _.bindControls = function() {
        $(document).keypress(function(event) {
            switch(event.which) {
                case  97: _.move({x: -1, y:  0}); break;
                case 100: _.move({x:  1, y:  0}); break;
                case 119: _.move({x:  0, y: -1}); break;
                case 115: _.move({x:  0, y:  1}); break;
            }
        });
    }
    
    /* schedule of long term tasks */
    _.scheduler = new function() { var scheduler = this
        scheduler.defer = function(fn, context) {
            setTimeout(function() {
                fn.call(context || window)
            }, 0)
        }
        
        var q = []
        var DEFAULT_TIME = 3
        var dequeuedimer
        scheduler.enqueue = function(fn, context, time) {
            var starttimer = (q.length == 0)
            q.push([fn, context, time])
            if(starttimer)
                dequeuedimer = setTimeout(dequeue, time?time:DEFAULT_TIME)
        }
        var dequeue = function() {
            if(q.length == 0) { return }            
            var e = q.shift()
            if(q.length != 0) {
                time = q[q.length-1][2]
                dequeuedimer = setTimeout(dequeue, time?time:DEFAULT_TIME)
            }
            e[0].call(e[1] || window)
        }
        scheduler.next = function() {
            if(q.length != 0) {
                clearTimeout(dequeuedimer)
                dequeue()
                //scheduler.defer(dequeue)
            }
        }
    }
}

/* functionality to import resources */
_import = new function() { _import = this;
    /*
     * tiledef import:
     *   tiledef = _import.tile({
     *      tile_xs: 1,   // tile width in tile-size-x-units
     *      tile_ys: 2    // tile height in tile-size-y-units
     *   }).pos ({
     *      x :  0,       // x start position of the tile in the tileset-file in tile-size-x-units
     *      xs : 16,      // number of tiles in x-direction
     *      y :  2,       // y start position of the tile in the tileset-file in tile-size-y-units
     *      ys:  1        // number of tiles in y-direction
     *   }).pos ({
     *      x :  0,       // x start position of the tile in the tileset-file in tile-size-x-units
     *      xs : 8,       // number of tiles in x-direction
     *      y :  5,       // y start position of the tile in the tileset-file in tile-size-y-units
     *      ys:  1        // number of tiles in y-direction
     *   });
     *
     * returns a datastructure for the coordinate for one tile in an image.
     * This is useable by _import.tileset to define a complete tileset for an image.
     *
     * .pos() - can be chained.
     * tile-size-?-units - a value in px set in _import.tileset
     *
     * tileset import:
     *   
     */
    _import.tile = function(defparams) {
        var t = new function() {};
        
        t.xs = defparams.tile_xs;
        t.ys = defparams.tile_ys;
        t.origin = defparams.origin;
            
        t.variant = [];
        t.pos = function(params) {
            var xoffset = params.x;
            var yoffset = params.y;
            for (y = 0; y < params.ys; y++) {
                for (x = 0; x < params.xs; x++) {
                    t.variant.push({
                        x  : x * t.xs + xoffset,
                        y  : y * t.ys + yoffset
                    });
                }
            }
            return t;
        }
        
        return t;
    }
    
    _import.tileset = function(name, params) {
        var tileset = new function() {};
        tileset.xs = params.xs;
        tileset.ys = params.ys;
        tileset.url = _.TILESET_DIR + params.url;
        
        for (var tilename in params.data) {
            var oldtile = params.data[tilename];
            var tile = [];
            
            tile.xs = oldtile.xs;
            tile.ys = oldtile.ys;
            tile.origin = oldtile.origin ? oldtile.origin : 0;
            tile.url = params.url;
            for (var variation in oldtile.variant) {
                tile.push({
                    x: oldtile.variant[variation].x * params.xs,
                    y: oldtile.variant[variation].y * params.ys
                });
            }
            
            tileset[tilename] = tile;
        }
        
        _.tileset[name] = tileset;
        return tileset;
    }
}
