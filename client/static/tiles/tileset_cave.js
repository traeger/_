_import.tileset('cave', {
    xs : 64,
    ys : 32,
    url : 'tileset_cave_1.png',
    data : {
        ground:     _import.tile({tile_xs: 1, tile_ys: 1})
                     .pos ({x :  0, xs : 16, y :  0, ys:  1}),
        trail:      _import.tile({tile_xs: 1, tile_ys: 1})
                     .pos ({x :  0, xs : 16, y :  1, ys:  1}),
        bones:      _import.tile({tile_xs: 1, tile_ys: 1})
                     .pos ({x :  0, xs : 8, y :  2, ys:  1})
    }
});
