from io import StringIO

import pytest

from mapparser.config import MapParserConfigReader, MapParserConfigException


@pytest.fixture
def basic_config_file():
    return StringIO(
        """
[MapParserConfig]
source_image = somefile.png
tile_size = 16 x24
output_tileset_name = mytiles.png
output_tile_map_name = mymap.json
    """
    )


@pytest.fixture
def bad_dimensions_config_file():
    return StringIO(
        """
[MapParserConfig]
source_image = somefile.png
tile_size = 16 b 24
output_tileset_name = mytiles.png
output_tile_map_name = mymap.json
    """
    )


@pytest.fixture
def missing_fields_config_file():
    return StringIO(
        """
[MapParserConfig]
source_image = somefile.png
tile_size = 16 x24
output_tile_map_name = mymap.json
    """
    )


@pytest.fixture
def missing_section_config_file():
    return StringIO(
        """
[Bleh]
source_image = somefile.png
tile_size = 16 x24
output_tileset_name = mytiles.png
output_tile_map_name = mymap.json
    """
    )


def test_parse_properties(basic_config_file):
    reader = MapParserConfigReader(basic_config_file)
    conf = reader.read_config()
    assert conf.source_image == "somefile.png"
    assert conf.tile_width == 16
    assert conf.tile_height == 24
    assert conf.output_tileset_name == "mytiles.png"
    assert conf.output_tile_map_name == "mymap.json"


def test_parse_malformed_dimensions_throws(bad_dimensions_config_file):
    with pytest.raises(MapParserConfigException):
        reader = MapParserConfigReader(bad_dimensions_config_file)
        conf = reader.read_config()


def test_missing_section_will_throw(missing_section_config_file):
    with pytest.raises(MapParserConfigException) as ex:
        reader = MapParserConfigReader(missing_section_config_file)
        conf = reader.read_config()
    assert "required section" in str(ex)


def test_missing_fields_will_throw(missing_fields_config_file):
    with pytest.raises(MapParserConfigException) as ex:
        reader = MapParserConfigReader(missing_fields_config_file)
        conf = reader.read_config()
    assert "output_tileset_name" in str(ex)
