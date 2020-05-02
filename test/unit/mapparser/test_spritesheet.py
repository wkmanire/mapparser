from unittest.mock import MagicMock, call

import pytest
from PIL import Image

from mapparser.spritesheet import (
    calculate_minimum_pot_size,
    calculate_minimum_tile_area,
    render_tiles,
)


def make_mock_image(width, height):
    image = MagicMock(spec=Image)
    image.width = width
    image.height = height
    return image


@pytest.fixture
def image_list():
    """
    Note: mapparser doen't support images of various sizes like this.
    In practice, they should all be uniform.  We are using different
    sizes here to help verify the math.
    """
    return [make_mock_image(5, 5), make_mock_image(2, 2), make_mock_image(7, 3)]


def test_calculate_minimum_tile_area(image_list):
    assert calculate_minimum_tile_area(image_list) == 25 + 4 + 21


def test_calculate_minimum_pot_size(image_list):
    image_list.append(make_mock_image(256, 256))
    assert calculate_minimum_pot_size(image_list) == 512


def test_render_tiles():
    """
    Should render a 2 by 3 tower of tiles.
    """
    images_list = [make_mock_image(16, 16) for i in range(6)]
    images = iter(images_list)
    sheet = MagicMock()
    render_tiles(images_list, sheet, 32)
    x = 16
    y = 16
    sheet.paste.assert_has_calls(
        [
            call(next(images), (x * 0, y * 0)),
            call(next(images), (x * 1, y * 0)),
            call(next(images), (x * 0, y * 1)),
            call(next(images), (x * 1, y * 1)),
            call(next(images), (x * 0, y * 2)),
            call(next(images), (x * 1, y * 2)),
        ],
        any_order=False,
    )
