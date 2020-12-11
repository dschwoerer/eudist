# distutils: language=c++

from libcpp cimport bool
from libcpp.string cimport string

cdef extern from "eudist_cpp.hxx":
    double dot_dot(double*, double*, int)
    cppclass Plane:
        Plane(double*, double*, double*, int)
        double dist(double *)
        double signed_dist(double *)
        void info()
    int winding_number(double*, double*, int)
    double polygon_dot(double*, double* , int, int, bool)

    cppclass PolyMesh:
        PolyMesh(double*, double*, int, int)
        int find_cell(double *, int)
