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
    a = np.ascontiguousarray(a)
    b = np.ascontiguousarray(b)
    return c.dot_dot(&a[0],&b[0],len(a))


cdef class Plane:
    """
    Defines a plane.

    The constructor takes 3 points
    """
    cdef c.Plane * cobj
    def __cinit__(self, np.ndarray[double,ndim=1] p0, np.ndarray[double,ndim=1] p1, np.ndarray[double,ndim=1] p2):
        p0 = np.ascontiguousarray(p0)
        p1 = np.ascontiguousarray(p1)
        p2 = np.ascontiguousarray(p2)
        self.cobj = new c.Plane(&p0[0], &p1[0], &p2[0], len(p0))

    def __dealloc__(self):
        self.__mydealloc__()

    def __mydealloc__(self):
        if self.cobj:
            del self.cobj
            self.cobj = NULL

    def dist(self, np.ndarray[double,ndim=1] dot):
        dot = np.ascontiguousarray(dot)
        return self.cobj.dist(&dot[0])

    def signed_dist(self, np.ndarray[double,ndim=1] dot):
        dot = np.ascontiguousarray(dot)
        return self.cobj.signed_dist(&dot[0])

    def info(self):
        self.cobj.info()

def plane_dot(Plane pl, np.ndarray[double, ndim=1] dot):
    return pl.dist(dot)

def winding_number(np.ndarray[double,ndim=2] points, np.ndarray[double, ndim=1] dot):
    cdef np.ndarray[double, ndim=1, mode='c'] pnts = np.ravel(points,order='c')
    dot = np.ascontiguousarray(dot)
    return c.winding_number(&pnts[0], &dot[0], len(points))

def polygon_dot(np.ndarray[double,ndim=2] points, np.ndarray[double, ndim=1] dot, check_planar=False):
    cdef np.ndarray[double, ndim=1, mode='c'] pnts = np.ravel(points,order='c')
    dot = np.ascontiguousarray(dot)
    return c.polygon_dot(&pnts[0], &dot[0], len(points), len(dot), check_planar)

