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


cdef class Plane:
    cdef c.Plane * cobj
    def __cinit__(self, np.ndarray[double,ndim=1] p0, np.ndarray[double,ndim=1] p1, np.ndarray[double,ndim=1] p2):
        self.cobj = new c.Plane(&p0[0], &p1[0], &p2[0], len(p0))

    def __dealloc__(self):
        self.__mydealloc__()

    def __mydealloc__(self):
        if self.cobj:
            del self.cobj
            self.cobj = NULL

    def dist(self, np.ndarray[double,ndim=1] dot):
        return self.cobj.dist(&dot[0])

def plane_dot(Plane pl, np.ndarray[double, ndim=1] dot):
    return pl.dist(dot)

def winding_number(np.ndarray[double,ndim=2, mode='c'] points, np.ndarray[double, ndim=1] dot):
    return c.winding_number(&points[0,0], &dot[0], len(points))

def polygon_dot(np.ndarray[double,ndim=2, mode='c'] points, np.ndarray[double, ndim=1] dot, check=False):
    return c.polygon_dot(&points[0,0], &dot[0], len(points), len(dot), check)
