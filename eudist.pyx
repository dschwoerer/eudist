# distutils: language=c++
# distutils: language_level=3
# distutils: include_dirs = 
# distutils: libraries = 
# distutils: library_dirs = 
# distutils: sources = eudist_cpp.cxx
# distutils: extra_compile_args =

cimport eudist_cpp as c
cimport numpy as np

def dot_dot(np.ndarray a, np.ndarray b):
    return c.dot_dot(a,b,len(a))
