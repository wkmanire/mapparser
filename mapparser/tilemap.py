from __future__ import annotations

from dataclasses import dataclass
from pprint import pformat
from typing import Tuple, Iterator, List, Optional
import json


class TileMap:
    def __init__(self, width: int, height: int):
        assert width > 0
        assert height > 0
        self.width = width
        self.height = height
        self.data = [[0 for x in range(self.width)] for y in range(self.height)]

    def yield_rect(
        self, rect: Optional[Tuple[int, int, int, int]] = None
    ) -> Iterator[int]:
        if rect is None:
            start_x, start_y, w, h = (0, 0, self.width, self.height)
        else:
            start_x, start_y, w, h = rect
            assert w <= self.width
            assert h <= self.height
            assert start_x >= 0
            assert start_y >= 0

        for y in range(start_y, h):
            for x in range(start_x, w):
                yield self.data[y][x]

    def populate_from_list(self, tile_ids: List[int]):
        assert len(tile_ids) == self.width * self.height
        tile_ids_iter = iter(tile_ids)
        for y in range(self.height):
            for x in range(self.width):
                self.data[y][x] = next(tile_ids_iter)

    def __getitem__(self, coords: Tuple[int, int]) -> int:
        x, y = coords
        if x < 0 or y < 0:
            return 0
        if x >= self.width or y >= self.height:
            return 0
        return self.data[y][x]

    def __setitem__(self, coords: Tuple[int, int], tile_id: int) -> None:
        x, y = coords
        assert x >= 0
        assert y >= 0
        assert x < self.width
        assert y < self.height
        self.data[y][x] = tile_id

    def __str__(self):
        return pformat(self.data)


@dataclass
class TileMapFileHeader:
    height: int = 0
    spritesheet: str = ""
    tile_height: int = 0
    tile_width: int = 0
    width: int = 0


class TileMapFile:
    def __init__(self, header: TileMapFileHeader, tile_map: TileMap):
        self.header: TileMapFileHeader = header
        self.tile_map: TileMap = tile_map

    def save_to_file(self, path: str):
        document = {
            "header": {
                "spritesheet": self.header.spritesheet,
                "height": self.header.height,
                "width": self.header.width,
                "tile_height": self.header.tile_height,
                "tile_width": self.header.tile_width,
            },
            "map": list(self.tile_map.yield_rect()),
        }
        with open(path, "w") as fob:
            json.dump(document, fob)

    @staticmethod
    def load(path: str) -> TileMapFile:
        with open(path, "r") as fob:
            data = json.load(fob)
        header = TileMapFileHeader()
        header_data = data["header"]
        header.height = header_data["height"]
        header.spritesheet = header_data["spritesheet"]
        header.tile_height = header_data["tile_height"]
        header.tile_width = header_data["tile_width"]
        header.width = header_data["width"]

        tile_map = TileMap(header.width, header.height)
        tile_map.populate_from_list(data["map"])
        return TileMapFile(header, tile_map)
