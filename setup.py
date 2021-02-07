from setuptools import Extension, setup

try:
    from Cython.Build import cythonize
except ImportError:
    # Ignore error, as otherwise setuptools doesn't know we need cython
    def cythonize(*args, **kwargs):
        pass


sourcefiles = ["eudist.pyx", "eudist_cpp.cxx"]

extensions = [Extension("eudist", sourcefiles)]

setup(
    use_scm_version=True,
    ext_modules=cythonize(
        extensions,
        language_level=3,
        compiler_directives=dict(binding=True, embedsignature=True),
    ),
)
