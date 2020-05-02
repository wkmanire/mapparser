# Map Parser CLI Utility

A utility that can read a screenshot/capture of a frame of a tiled game and produce a tileset and map file from it. This is a fairly niche utility that would only be useful in very specific circumstances. As such, I'm not making it available on pypi.

## Installing

mapparser requires python 3.8 or newer.

### Using a Release

Download a release wheel and install it using pip.

pip install --user ./[WHEEL NAME]

### Installing from Source

1. Clone this repo
  1. git clone https://github.com/wkmanire/mapparser
2. Checkout a release tag
  1. git checkout v1.0.0
3. Install the requirements from both requirements.txt and requirements-dev.txt
  1. python -m pip install --user -r requirements.txt
  2. python -m pip install --user -r requirements-dev.txt
4. Build a wheel distribution
  1. python setup.py bdist_wheel




