from setuptools import Extension, setup
from Cython.Build import cythonize

sourcefiles = ["eudist.pyx", "eudist_cpp.cxx"]
# , 'helper.c', 'another_helper.c']

extensions = [Extension("eudist", sourcefiles)]

setup(
    name="eudist",
    version="0.1.1",
    ext_modules=cythonize(
        extensions,
        language_level=3,
        compiler_directives=dict(binding=True, embedsignature=True),
    ),
)
