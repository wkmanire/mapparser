from typing import Tuple
import configparser
import re
from dataclasses import dataclass, fields


class MapParserConfigException(Exception):
    pass


@dataclass
class MapParserConfig:
    source_image: str = ""
    tile_width: int = 0
    tile_height: int = 0
    output_tileset_name: str = ""
    output_tile_map_name: str = ""


class MapParserConfigReader:
    DIMENSION_STRING = re.compile(r"^(?P<width>\d+)\s*x\s*(?P<height>\d+)$")

    def __init__(self, config_file):
        self.config_file = config_file

    def read_config(self) -> MapParserConfig:
        parser = configparser.ConfigParser()
        parser.read_file(self.config_file)
        self.validate_config(parser)
        conf = MapParserConfig()
        conf.source_image = parser[MapParserConfig.__name__]["source_image"]
        conf.output_tileset_name = parser[MapParserConfig.__name__][
            "output_tileset_name"
        ]
        conf.output_tile_map_name = parser[MapParserConfig.__name__][
            "output_tile_map_name"
        ]
        dimension_string = parser[MapParserConfig.__name__]["tile_size"]
        conf.tile_width, conf.tile_height = self.parse_tile_dimensions(dimension_string)
        return conf

    @staticmethod
    def validate_config(parser) -> None:
        if not parser.has_section(MapParserConfig.__name__):
            raise MapParserConfigException(
                f"Missing required section in config {MapParserConfig.__name__}"
            )
        for field_name in [f.name for f in fields(MapParserConfig())]:
            if (
                "width" not in field_name
                and "height" not in field_name
                and not parser.has_option(MapParserConfig.__name__, field_name)
            ):
                raise MapParserConfigException(
                    f"Missing required option in config {field_name}"
                )

    @staticmethod
    def parse_tile_dimensions(dimension_string) -> Tuple[int, int]:
        m = MapParserConfigReader.DIMENSION_STRING.match(dimension_string.strip())
        if m:
            return int(m.group("width")), int(m.group("height"))
        raise MapParserConfigException(
            f"tile_size must be in the format 'WIDTHxHEIGHT' but was '{dimension_string}'"
        )
