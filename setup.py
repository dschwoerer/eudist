from setuptools import Extension, setup
from Cython.Build import cythonize

sourcefiles = ["eudist/__init__.pyx"]
#, 'helper.c', 'another_helper.c']

extensions = [Extension("eudist", sourcefiles)]

setup(
    ext_modules=cythonize(extensions, language_level=3)
)
