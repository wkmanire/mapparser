from typing import List, Any

from PIL import Image


def render(tiles: List[Any]) -> Image:
    """Render a list of tile images into a spritesheet.

    The resulting spritesheet will be automatically sized to be the
    smallest power of two sized image that contain all of the tiles.
    It is assumed that all of the tiles have the same dimensions,
    though the tiles do not need to be perfectly square.
    """
    pot_side_length = calculate_minimum_pot_size(tiles)
    sprite_sheet = Image.new(tiles[0].mode, (pot_side_length, pot_side_length))
    render_tiles(tiles, sprite_sheet, sprite_sheet.width)
    return sprite_sheet


def calculate_minimum_pot_size(tiles: List[Any]) -> int:
    """Return the side length of the smallest perfect square that can
    contain all of the images in the tiles list, where the side length
    is a power of 2.
    """
    min_area = calculate_minimum_tile_area(tiles)
    pot_area = 0
    pot_side_length = 0
    power = 0
    while pot_area < min_area:
        pot_side_length = 2 ** power
        pot_area = pot_side_length ** 2
        power += 1
    return pot_side_length


def calculate_minimum_tile_area(tiles: List[Any]) -> int:
    """
    Return the sum of the area of all of the images in the tiles list.
    """
    return sum(t.width * t.height for t in tiles)


def render_tiles(tiles: List[Any], sheet: Image, max_width: int) -> None:
    """
    Render every image in the tiles list from left to right, top to
    bottom.
    """
    x, y = 0, 0
    for tile in tiles:
        sheet.paste(tile, (x, y))
        if x + tile.width >= max_width:
            x = 0
            y += tile.height
        else:
            x += tile.width
