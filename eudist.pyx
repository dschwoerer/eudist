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
    """
    Distance between two dots.
    """
    a = np.ascontiguousarray(a)
    b = np.ascontiguousarray(b)
    return c.dot_dot(&a[0],&b[0],len(a))


cdef class Plane:
    """
    Defines a plane.

    The constructor takes 3 points that are on the plane and span the plane.
    """
    cdef c.Plane * cobj
    def __cinit__(self, np.ndarray[double,ndim=1] p0, np.ndarray[double,ndim=1] p1, np.ndarray[double,ndim=1] p2):
        p0 = np.ascontiguousarray(p0)
        p1 = np.ascontiguousarray(p1)
        p2 = np.ascontiguousarray(p2)
        self.cobj = new c.Plane(&p0[0], &p1[0], &p2[0], len(p0))

    def __dealloc__(self):
        Plane._eudist_dealloc(self)

    def _eudist_dealloc(self):
        if self.cobj:
            del self.cobj
            self.cobj = NULL

    def dist(self, np.ndarray[double,ndim=1] dot):
        """
        Distance between the plane and the given point.
        """
        dot = np.ascontiguousarray(dot)
        return self.cobj.dist(&dot[0])

    def signed_dist(self, np.ndarray[double,ndim=1] dot):
        """
        Signed distance between the plane and the given point.

        While the sign is depending on the order of the given points and is
        thus to some extend abitrary. However, if the sign of two points is
        different, they are on different sides of the plane.
        """
        dot = np.ascontiguousarray(dot)
        return self.cobj.signed_dist(&dot[0])

    def info(self):
        """
        Print some info about the Plane. Mostly for debugging.
        """
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
                raise ValueError(f"Data mismatch: ({xs[0]}, {xs[1]}) != ({ys[0]}, {ys[1]})")
        cdef np.ndarray[double, ndim=1, mode='c'] datax_ = np.ravel(datax, order='c')
        cdef np.ndarray[double, ndim=1, mode='c'] datay_ = np.ravel(datay, order='c')
        self.cobj = new c.PolyMesh(&datax_[0], &datay_[0], datax.shape[0], datay.shape[1])

    def __dealloc__(self):
        PolyMesh._eudist_dealloc(self)

    def _eudist_dealloc(self):
        if self.cobj:
            del self.cobj
            self.cobj = NULL

    def find_cell(self,  np.ndarray[double,ndim=1] dot, int guess=-1):
        """
        Find the cellid for a given point.
        """
        dot = np.ascontiguousarray(dot)
        return self.cobj.find_cell(&dot[0], guess)

def plane_dot(Plane pl, np.ndarray[double, ndim=1] dot):
    """
    Calculate the distance between the Plane and a dot
    """
    return pl.dist(dot)

def winding_number(np.ndarray[double,ndim=2] points, np.ndarray[double, ndim=1] dot):
    """
    Calculate the winding number between the 2-d surface spawened by
    the `points` and the `dot`.  A winding number of zero means the
    point is outside the surface.

    The shape of `points` has to be `(n, 2)`.

    If the conversions are slow, ensure the variables are already
    C-contigous, e.g. with `assert points.flags['C_CONTIGUOUS']`
    """
    assert points.shape[1] == 2
    cdef np.ndarray[double, ndim=1, mode='c'] pnts = np.ravel(points,order='c')
    dot = np.ascontiguousarray(dot)
    return c.winding_number(&pnts[0], &dot[0], len(points))


def polygon_dot(np.ndarray[double,ndim=2] points, np.ndarray[double, ndim=1] dot, check_planar=False):
    """
    Calculate the distance between a polygon and a dot.

    The polygon is assumed to be flat.
    """
    cdef np.ndarray[double, ndim=1, mode='c'] pnts = np.ravel(points,order='c')
    dot = np.ascontiguousarray(dot)
    return c.polygon_dot(&pnts[0], &dot[0], len(points), len(dot), check_planar)



def _det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def _vlen(a):
    return np.sqrt(np.dot(a, a))


def do_seg_seg_intersect(seq0, seq1):
    """
    Check if the two line segments intersect.
    """
    eps = 1e-16
    v0 = seq0[1] - seq0[0]
    v1 = seq1[1] - seq1[0]
    p0 = seq0[0]
    p1 = seq1[0]
    dist = p1 - p0

    det1 = _det(v0, v1)
    # check for co-linearity:
    if abs(det1) < eps:
        # Check for overlap? - not yet
        # dist -= np.dot(dist, v0) / _vlen(v0) / _vlen(dist)
        # print("colin", dist, det1)
        return False

    t0 = _det(dist, v0) / det1

    if t0 < -eps or t0 > 1 + eps:
        # print("t0", t0)
        return False

    t1 = _det(dist, v1) / det1

    if t1 < -eps or t1 > 1 + eps:
        # print("t1", t1)
        return False

    return True

include "eudist/_version.py"
