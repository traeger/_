_import.tileset('grassland_ramp', {
    xs : 64,
    ys : 32,
    url : 'grassland_ramp.png',
    data : {
        cliff: _import.tile({tile_xs: 1, tile_ys: 3})
                     .pos ({x :  0, xs : 16, y :  1, ys:  1})
                     .pos ({x :  0, xs :  8, y :  5, ys:  1})
    }
});
