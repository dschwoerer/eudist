# distutils: language=c++

from libcpp cimport bool
from libcpp.string cimport string

cdef extern from "eudist_cpp.hxx":
     cdef double dot_dot(double*, double*, int)

