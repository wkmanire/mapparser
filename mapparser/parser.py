from typing import List, Tuple, Any
from dataclasses import dataclass, field
from operator import itemgetter

from PIL import Image
from .config import MapParserConfig


@dataclass
class ParseResult:
    tiles: List[Any] = field(default_factory=list)
    map_data: List[int] = field(default_factory=list)
    num_cols: int = 0
    num_rows: int = 0


class TileDimensionException(Exception):
    pass


class TileReader:
    def __init__(self, source_image: Image, tile_size: Tuple[int, int]):
        self.image = source_image
        self.tile_width, self.tile_height = tile_size

    def __iter__(self):
        max_row, max_col = self.get_max_row_and_col()
        for row in range(0, max_row):
            for col in range(0, max_col):
                box = self.calculate_tile_box(col, row)
                yield self.image.crop(box)

    def get_max_row_and_col(self):
        width_in_px, height_in_px = self.image.size
        if width_in_px % self.tile_width != 0:
            raise TileDimensionException(
                "The specified tile width is not a multiple of the source image width"
            )
        if height_in_px % self.tile_height != 0:
            raise TileDimensionException(
                "The specified tile height is not a multiple of the source image height"
            )
        max_col = width_in_px // self.tile_width
        max_row = height_in_px // self.tile_height
        return (max_row, max_col)

    def calculate_tile_box(self, col: int, row: int):
        box_left = col * self.tile_width
        box_top = row * self.tile_height
        box_right = box_left + self.tile_width
        box_bottom = box_top + self.tile_height
        return (box_left, box_top, box_right, box_bottom)


class TileIndex:
    def __init__(self):
        self.index = dict()
        self.next_tile_id = 1

    def index_tile(self, tile_image: Image) -> int:
        tile_string = tile_image.tobytes()
        tile_id: int = 0
        if tile_string not in self.index:
            self.index[tile_string] = self.next_tile_id
            tile_id = self.next_tile_id
            self.next_tile_id += 1
        else:
            tile_id = self.index[tile_string]
        return tile_id

    def __iter__(self):
        for pair in sorted(self.index.items(), key=itemgetter(1)):
            key, value = pair
            yield (value, key)


class Parser:
    def __init__(
        self, config: MapParserConfig, tile_reader: TileReader, tile_index: TileIndex
    ):
        self.config: MapParserConfig = config
        self.index = tile_index
        self.map_data: List[int] = list()
        self.reader = tile_reader

    @staticmethod
    def parse_image(config: MapParserConfig) -> ParseResult:
        source_image = Image.open(config.source_image).convert("RGBA")
        tile_size = (config.tile_width, config.tile_height)
        reader = TileReader(source_image, tile_size)
        index = TileIndex()
        parser = Parser(config, reader, index)
        return parser.parse(source_image, tile_size)

    def parse(self, source_image: Image, tile_size: Tuple[int, int]) -> ParseResult:
        for tile in self.reader:
            tile_id = self.index.index_tile(tile)
            self.map_data.append(tile_id)
        result = ParseResult()
        result.map_data = self.map_data[:]
        result.tiles = [
            Image.frombytes(source_image.mode, tile_size, pixel_data)
            for _, pixel_data in iter(self.index)
        ]
        result.num_cols = source_image.size[0] // tile_size[0]
        result.num_rows = source_image.size[1] // tile_size[1]
        return result
