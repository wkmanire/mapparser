from PIL import Image

from mapparser.spritesheet import render


def test_render():
    fill_color = (255, 0, 0, 255)
    empty = (0, 0, 0, 0)
    tiles = [Image.new("RGBA", (16, 16), color=fill_color) for i in range(26)]
    sheet = render(tiles)
    assert sheet.height == 128
    assert sheet.width == 128
    assert sheet.getpixel((0, 0)) == fill_color
    assert sheet.getpixel((32, 32)) == fill_color
    assert sheet.getpixel((32, 48)) == empty
