# distutils: language=c++
# distutils: include_dirs = /u/dave/local/python3.9/lib/python3.9/site-packages/numpy/core/include
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

cdef class PolyMesh:
    """
    Defines a mesh in 2 dimension, which allows for fast finding of in which cell a point is.

    The constructor takes two 2D array for the x and y position of the grid corners.
    """
    cdef c.PolyMesh * cobj
    def __cinit__(self, np.ndarray[double,ndim=2] datax, np.ndarray[double,ndim=2] datay):
        for i in range(2):
            if not datax.shape[i] == datay.shape[i]:
                xs = datax.shape
                ys = datay.shape
                print(f"Data mismatch: ({xs[0]}, {xs[1]}) != ({ys[0]}, {ys[1]})")
        cdef np.ndarray[double, ndim=1, mode='c'] datax_ = np.ravel(datax, order='c')
        cdef np.ndarray[double, ndim=1, mode='c'] datay_ = np.ravel(datay, order='c')
        self.cobj = new c.PolyMesh(&datax_[0], &datay_[0], datax.shape[0], datay.shape[1])

    def __dealloc__(self):
        self.__mydealloc__()

    def __mydealloc__(self):
        if self.cobj:
            del self.cobj
            self.cobj = NULL

    def find_cell(self,  np.ndarray[double,ndim=1] dot, int guess=-1):
        """
        Find the cellid of a point.
        """
        dot = np.ascontiguousarray(dot)
        return self.cobj.find_cell(&dot[0], guess)

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
