from distutils.core import setup
from setuptools import find_packages


setup(
    name='MangaUpdatesFeedFilter',
    version='0.1',
    description='Generates a manga RSS feed filtered to a users list',
    packages=find_packages(),
    python_requires='>=3.4',
    install_requires=['requests','lxml']
)