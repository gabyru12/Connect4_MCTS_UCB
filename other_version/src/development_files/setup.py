# setup.py
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("connect4API.pyx", language_level=3)
)