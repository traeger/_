"""
Licensed under The MIT License (MIT)
Copyright (c) 2013 Marco Träger <marco.traeger at googlemail.com>
This file is part of the game _ and the _.py gameserver (https://github.com/traeger/_).

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
"""

CHUNK_SIZE = 8
CHUNK_DIMS = 3
CHUNK_DIM_TERRAIN = 0
CHUNK_DIM_HEIGHT  = 1
CHUNK_DIM_OBJECTS = 2

"""
world height generation.

half of the generated positiv heights are be between
0 and 'WORLD_HEIGHT_HALF' and the other half between
'WORLD_HEIGHT_HALF' and 'WORLD_HEIGHT_MAX'.

In the implementation via simplex-noise a quadratic 
interpolation is used.
"""
WORLD_HEIGHT_HALF = 300
WORLD_HEIGHT_MAX = 8000

REGION_HEIGHT_HALF = 5
REGION_HEIGHT_MAX  = 40

LOCAL_HEIGHT_HALF = 2
LOCAL_HEIGHT_MAX  = 5