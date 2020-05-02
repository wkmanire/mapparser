import pytest

from io import StringIO
from argparse import ArgumentParser
from unittest.mock import patch, MagicMock

from mapparser.app import App


@pytest.fixture
def basic_config_file():
    return StringIO(
        """
[MapParserConfig]
source_image = somefile.png
tile_size = 16x16
output_tileset_name = mytiles.png
output_tile_map_name = mymap.json
    """
    )


@patch("mapparser.app.ArgumentParser", spec=ArgumentParser)
def test_app_constructor_reads_config_from_cmd_args(
    MockArgumentParser, basic_config_file
):
    arg_parser = MockArgumentParser.return_value
    mock_args = MagicMock()
    arg_parser.parse_args.return_value = mock_args
    mock_args.config = basic_config_file
    app = App.new()
    assert app.config.source_image == "somefile.png"
