"""Defines the main application class for map parser."""

from __future__ import annotations

from argparse import ArgumentParser, FileType
from logging import getLogger

from .config import MapParserConfigReader, MapParserConfig
from .parser import Parser
from .spritesheet import render
from .tilemap import TileMapFile, TileMapFileHeader, TileMap

LOGGER = getLogger(__name__)


class App:
    def __init__(self, config: MapParserConfig):
        self.config = config

    @staticmethod
    def new() -> App:
        arg_parser = ArgumentParser(prog="MapParser")
        arg_parser.add_argument(
            "--config",
            required=True,
            type=FileType("r"),
            help="Path to config file specifying how to read the map image.",
        )
        args = arg_parser.parse_args()
        conf_parser = MapParserConfigReader(args.config)
        conf = conf_parser.read_config()
        app = App(conf)
        return app

    def run(self) -> None:
        LOGGER.debug("Starting up")
        result = Parser.parse_image(self.config)
        image = render(result.tiles)
        image.save(self.config.output_tileset_name, "PNG")
        tile_map = TileMap(result.num_cols, result.num_rows)
        tile_map.populate_from_list(result.map_data)
        header = TileMapFileHeader()
        header.height = tile_map.height
        header.width = tile_map.width
        header.tile_width = self.config.tile_width
        header.tile_height = self.config.tile_height
        header.spritesheet = self.config.output_tileset_name
        tile_map_file = TileMapFile(header, tile_map)
        tile_map_file.save_to_file(self.config.output_tile_map_name)
