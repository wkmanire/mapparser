import pytest
from mapparser.tilemap import TileMap


def test_tilemap_get_and_set():
    tilemap = TileMap(5, 5)
    tilemap[2, 2] = 15
    assert tilemap[2, 2] == 15


def test_tilemap_yield_rect():
    tilemap = TileMap(5, 5)
    i = 0
    for y in range(5):
        for x in range(5):
            tilemap[x, y] = i
            i += 1
    print(tilemap)
    last = -1
    for value in tilemap.yield_rect((0, 0, 5, 5)):
        assert last == value - 1
        last = value


def test_tilemap_get_out_of_bounds_yields_zero():
    assert TileMap(5, 5)[300, 200] == 0
    assert TileMap(5, 5)[-300, -200] == 0


def test_tilemap_set_out_of_bounds_raises():
    tilemap = TileMap(5, 5)
    with pytest.raises(AssertionError):
        tilemap[-1, -1] = 1
    with pytest.raises(AssertionError):
        tilemap[0, -1] = 1
    with pytest.raises(AssertionError):
        tilemap[-1, 0] = 1
    with pytest.raises(AssertionError):
        tilemap[6, 0] = 1
    with pytest.raises(AssertionError):
        tilemap[0, 6] = 1
