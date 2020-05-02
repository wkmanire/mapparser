from PIL import Image
from os.path import split, join
from subprocess import check_output
import json
import os


def test_end_to_end():
    cwd = split(__file__)[0]
    check_output(
        "python -m mapparser --config test_end_to_end.ini".split(" "), cwd=cwd,
    )
    try:
        expected_map = json.loads(
            open(join(cwd, "test_end_to_end_tile_map.json")).read()
        )
        assert expected_map == {
            "header": {
                "spritesheet": "test_end_to_end_tileset.png",
                "height": 2,
                "width": 2,
                "tile_height": 32,
                "tile_width": 32,
            },
            "map": [1, 2, 3, 4],
        }
        # The created tileset should be exactly identical to the input tile map image
        expected = Image.open(join(cwd, "test_end_to_end.png"))
        actual = Image.open(join(cwd, "test_end_to_end_tileset.png"))
        assert expected.tobytes() == actual.tobytes()
    except AssertionError as ex:
        os.remove(join(cwd, "test_end_to_end_tileset.png"))
        os.remove(join(cwd, "test_end_to_end_tile_map.json"))
        raise ex
    finally:
        os.remove(join(cwd, "test_end_to_end_tileset.png"))
        os.remove(join(cwd, "test_end_to_end_tile_map.json"))
