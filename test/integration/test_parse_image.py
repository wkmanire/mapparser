from unittest.mock import patch, MagicMock

from mapparser.parser import Parser
from mapparser.config import MapParserConfig


def make_mock_tile(bytes_data):
    instance = MagicMock()
    instance.tobytes.return_value = bytes_data
    return instance


@patch("mapparser.parser.Image")
def test_parse_image(mock_image_class):
    """Find 3 different tiles on a 4 tile wide map"""
    mock_image_class.frombytes = lambda _1, _2, s: s
    instance = MagicMock()
    instance.size = (64, 16)
    # tile-3 is intentionally repeated
    instance.crop.side_effect = [
        make_mock_tile(b"tile-1"),
        make_mock_tile(b"tile-2"),
        make_mock_tile(b"tile-3"),
        make_mock_tile(b"tile-3"),
    ]
    mock_image_class.open.return_value.convert.return_value = instance
    conf = MapParserConfig()
    conf.tile_width = 16
    conf.tile_height = 16
    result = Parser.parse_image(conf)
    assert [1, 2, 3, 3] == result.map_data
    assert [b"tile-1", b"tile-2", b"tile-3"] == result.tiles
    assert 4 == result.num_cols
    assert 1 == result.num_rows
