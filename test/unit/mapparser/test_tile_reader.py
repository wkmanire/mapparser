from unittest.mock import MagicMock
import pytest

from PIL import Image

from mapparser.parser import TileReader, TileDimensionException


def test_tile_reader_raises_if_width_not_factor_of_image_size():
    image = MagicMock()
    image.size = (72, 32)
    tile_size = (16, 16)
    reader = TileReader(image, tile_size)
    with pytest.raises(TileDimensionException) as ex:
        reader.get_max_row_and_col()
    assert "width is not a multiple" in str(ex)


def test_tile_reader_raises_if_height_not_factor_of_image_size():
    image = MagicMock()
    image.size = (32, 133)
    tile_size = (16, 16)
    reader = TileReader(image, tile_size)
    with pytest.raises(TileDimensionException) as ex:
        reader.get_max_row_and_col()
    assert "height is not a multiple" in str(ex)


@pytest.mark.parametrize("col,row,box", [(0, 0, (0, 0, 16, 15)),
                                         (1, 1, (16, 15, 32, 30)),
                                         (3, 5, (48, 75, 64, 90))])
def test_tile_reader_calculates_crop_box(col, row, box):
    reader = TileReader(None, (16, 15))
    assert box == reader.calculate_tile_box(col, row)


def test_yield_tiles_from_source_image():
    image = MagicMock()
    image.size = (256, 256)
    reader = TileReader(image, (16, 16))
    assert len([t for t in reader]) == 256
