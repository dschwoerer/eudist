from setuptools import Extension, setup
import os

incdir = ""
try:
    from Cython.Build import cythonize
    import numpy as np

    import setuptools_scm as ver

    incdir = np.get_include()

    try:
        with open("eudist/_version.py") as f:
            pass
    except FileNotFoundError:
        version = ver.get_version()
        with open("eudist/_version.py", "w") as f:
            f.write(
                f"""# coding: utf-8
# file generated by setuptools_scm
# don't change, don't track in version control
__version__ = version = {repr(version)}
__version_tuple__ = version_tuple = ({', '.join([repr(x) for x in version.split('.')])})
"""
            )
except ImportError:
    # For some reason setuptool does not install cython, so it is better to error out
    raise
    # Ignore error, as otherwise setuptools doesn't know we need cython
    def cythonize(*args, **kwargs):
        pass


sourcefiles = ["eudist.pyx", "eudist_cpp.cxx"]

if os.name == "nt":
    extra_compile_args = ["/TP", "/permissive-"]
else:
    extra_compile_args = ["-std=c++11"]

extensions = [
    Extension(
        "eudist",
        sourcefiles,
        include_dirs=[incdir],
        extra_compile_args=extra_compile_args,
    )
]

setup(
    use_scm_version=True,
    ext_modules=cythonize(
        extensions,
        language_level=3,
        compiler_directives=dict(binding=True, embedsignature=True),
    ),
    setup_requires=[
        "setuptools>=42",
        "setuptools_scm[toml]>=3.4",
        "setuptools_scm_git_archive",
        "numpy",
        "cython",
    ],
    install_requires=[
        "numpy",
    ],
)
