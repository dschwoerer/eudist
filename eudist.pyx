# distutils: language=c++
# distutils: include_dirs = 
# distutils: libraries = 
# distutils: library_dirs = 
# distutils: sources = eudist_cpp.cxx
# distutils: extra_compile_args =

cimport eudist_cpp as c
cimport numpy as np
import numpy as np

def dot_dot(np.ndarray[double,ndim=1] a, np.ndarray[double, ndim=1] b):
    #assert a.shape == b.shape
    #assert a.dtype == b.dtype == float
    return c.dot_dot(&a[0],&b[0],len(a))

