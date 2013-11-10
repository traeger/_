_import.tileset('terrain_grass', {
    xs : 64,
    ys : 32,
    url : 'tileset_terrain_grass.png',
    data : {
        floor:      _import.tile({tile_xs: 1, tile_ys: 4})
                     .pos ({x :  0, xs :  8, y :  0, ys:  1}),
        water:      _import.tile({tile_xs: 1, tile_ys: 4})
                     .pos ({x :  8, xs :  8, y :  0, ys:  1}),
        cliff2:     _import.tile({tile_xs: 1, tile_ys: 4})
                     .pos ({x :  0, xs : 12, y :  4, ys:  1}),
        cliff1:     _import.tile({tile_xs: 1, tile_ys: 4})
                     .pos ({x : 12, xs :  4, y :  4, ys:  1})
                     .pos ({x :  0, xs :  8, y :  8, ys:  1}),
        ramp:       _import.tile({tile_xs: 1, tile_ys: 4})
                     .pos ({x :  8, xs :  8, y :  8, ys:  1})
                     .pos ({x :  0, xs :  4, y : 12, ys:  1}),
        fade:       _import.tile({tile_xs: 1, tile_ys: 4})
                     .pos ({x :  4, xs :  8, y : 12, ys:  1}),       
    }
});
