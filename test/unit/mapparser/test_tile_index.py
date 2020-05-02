from unittest.mock import MagicMock

from mapparser.parser import TileIndex


def make_mock_tile(bytes_data):
    instance = MagicMock()
    instance.tobytes.return_value = bytes_data
    return instance


def test_index_images_and_return_them_by_id_order():
    index = TileIndex()
    index.index_tile(make_mock_tile(b"test-1"))
    index.index_tile(make_mock_tile(b"test-2"))
    index.index_tile(make_mock_tile(b"test-2"))
    index.index_tile(make_mock_tile(b"test-2"))
    index.index_tile(make_mock_tile(b"test-3"))
    index.index_tile(make_mock_tile(b"test-2"))
    index.index_tile(make_mock_tile(b"test-1"))
    expected = [(1, b"test-1"), (2, b"test-2"), (3, b"test-3")]
    assert expected == list(index)
