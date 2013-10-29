_import.tileset('grassland', {
    xs : 64,
    ys : 32,
    url : 'grassland_tiles.png',
    data : {
        grass:      _import.tile({tile_xs: 1, tile_ys: 1})
                     .pos ({x :  0, xs : 16, y :  0, ys:  1}),
        path:       _import.tile({tile_xs: 1, tile_ys: 1})
                     .pos ({x :  0, xs : 16, y :  1, ys:  1}),
        cliff:      _import.tile({tile_xs: 1, tile_ys: 3})
                     .pos ({x :  0, xs : 16, y :  2, ys:  1})
                     .pos ({x :  0, xs :  8, y :  5, ys:  1}),
        water:      _import.tile({tile_xs: 1, tile_ys: 1})
                     .pos ({x :  0, xs : 16, y :  19, ys:  1}),
        watercliff: _import.tile({tile_xs: 1, tile_ys: 2, origin: 1})
                     .pos ({x :  0, xs : 16, y :  15, ys:  1})
                     .pos ({x :  0, xs :  8, y :  17, ys:  1}),
        rock:       _import.tile({tile_xs: 1, tile_ys: 3})
                     .pos ({x :  0, xs :  8, y : 12, ys:  1}),
        pine:       _import.tile({tile_xs: 2, tile_ys: 6})
                     .pos ({x :  0, xs :  4, y : 36, ys:  1}),
        oak:        _import.tile({tile_xs: 2, tile_ys: 5})
                     .pos ({x :  8, xs :  4, y : 37, ys:  1})
    }
});
