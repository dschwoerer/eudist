#include "eudist_cpp.hxx"
#include <cmath>

double dot_dot(double *a, double *b, int n) {
  double result = 0;
  for (int i = 0; i < n; ++i) {
    auto diff = a[i] - b[i];
    result += diff * diff;
  }
  return result;
}

double dot_prod(double *a, double *b, int n) {
  double result = 0;
  for (int i = 0; i < n; ++i) {
    result += a[i] * b[i];
  }
  return result;
}

Plane::Plane(double *p0, double *p1, double *p2, int n)
    : dim(n), norm(nullptr) {
  if (dim == 3) {
    double v0[dim], v1[dim];
    for (int i = 0; i < dim; ++i) {
      v0[i] = p1[i] - p0[i];
      v1[i] = p2[i] - p0[i];
    }
    norm = new double[dim];
    norm[0] = v0[1] * v1[2] - v0[2] * v1[1];
    norm[1] = v0[2] * v1[0] - v0[0] * v1[2];
    norm[2] = v0[0] * v1[1] - v0[1] * v1[0];
    d = 0;
    normsq = 0;
    for (int i = 0; i < dim; ++i) {
      d -= norm[i] * p0[i];
      normsq += norm[i] * norm[i];
    }
    normlen = sqrt(normsq);
  }
}

Plane::~Plane() { delete[] norm; }

double Plane::dist(double *dot) {
  if (dim == 2) {
    return 0.;
  }
  return (dot_prod(dot, norm, dim) + d) / normlen;
}
