from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mapparser",
    version="1.0.0",
    description="Create spritesheets and tilemaps from screen captures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wkmanire/mapparser",
    author="wkmanire",
    author_email="williamkmanire@gmail.com",
    packages=["mapparser"],
    python_requires=">=3.8",
    install_requires=[],
    entry_points={"console_scripts": ["mapparser=mapparser.__main__:main",],},
)
