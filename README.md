# Map Parser CLI Utility

A utility that can read a screenshot/capture of a frame of a tiled game and produce a tileset and map file from it. This is a fairly niche utility that would only be useful in very specific circumstances. As such, I'm not making it available on pypi.

## Installing

mapparser is only tested with python 3.8 or newer. It may work with earlier versions of python 3.x however don't even try to run this in python 2.x.

### Dependencies

mapparser only has one runtime dependency: Pillow. Make sure pillow is installed before following the installation instructions below or it won't work when you run it.

```bash
python3 -m pip install --user Pillow
```

### Using a Release

Download a release wheel and install it using pip. Be sure to replace the X placeholders with the version numbers of whichever release you downloaded.

```bash
python3 -m pip install --user mapparser-x.x.x-py3-none-any.whl
```
pip install --user ./[WHEEL NAME]

### Installing from Source

1. Clone this repo
  1. git clone https://github.com/wkmanire/mapparser
2. Checkout a release tag
  1. git checkout v1.0.0
3. Install the requirements from both requirements.txt
  1. `python -m pip install --user -r requirements.txt`
  2. OPTIONAL: Install dev dependencies if you want to run the unit tests
    1. `python -m pip install --user -r requirements-dev.txt`
	2. To run the tests `pytest` in the root of the repository
4. Build a wheel distribution
  1. `python setup.py bdist_wheel`
5. Install the wheel either globally or in your home directory
  1. `python -m pip install --user dist/mapparser-x.x.x-py3-none-any.whl`

## Using mapparser

```
usage: MapParser [-h] --config CONFIG

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  Path to config file specifying how to read the map image.
```

To run mapparser you first need to find a source image and setup a config file **for that specific image**. There is a sample config file in the functional test folder. All of the fields are required.

```ini
[MapParserConfig]
# The image to read the tiles from
source_image = my_source_image.png

# The size of the tiles in the source image
tile_size = 32x32

# The name of the image to write the tileset to
output_tileset_name = my_tileset.png

# The name of the file to write the map data to
output_tile_map_name = my_map.json
```

If everything worked, there will be no output text.

```
$ mapparser --config myconfig.ini
$ ls
my_source_image.png    my_tileset.png    my_map.json
```

