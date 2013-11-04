_import.tileset('grassland_floor', {
    xs : 64,
    ys : 32,
    url : 'grassland_floor.png',
    data : {
        grass: _import.tile({tile_xs: 1, tile_ys: 1})
                     .pos ({x :  0, xs : 16, y :  0, ys:  1})
    }
});
