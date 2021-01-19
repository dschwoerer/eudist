#include "eudist_cpp.hxx"
#include <cmath>
#include <stdexcept>

double dot_dot(const double *a, const double *b, int n) {
  double result = 0;
  for (int i = 0; i < n; ++i) {
    auto diff = a[i] - b[i];
    result += diff * diff;
  }
  return sqrt(result);
}

double dot_prod(const double *a, const double *b, int n) {
  double result = 0;
  for (int i = 0; i < n; ++i) {
    result += a[i] * b[i];
  }
  return result;
}

Plane::Plane(const double *p0, const double *p1, const double *p2, int n)
    : norm(nullptr), dim(n) {
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

double Plane::dist(const double *dot) {
  if (dim == 2) {
    return 0.;
  }
  return fabs(dot_prod(dot, norm, dim) + d) / normlen;
}

double Plane::signed_dist(const double *dot) {
  if (dim == 2) {
    return 0.;
  }
  return (dot_prod(dot, norm, dim) + d) / normlen;
}

void Plane::info() {
  printf("Dim: %d\n", dim);
  printf("Norm: %.4f %.4f %.4f\n", norm[0], norm[1], norm[2]);
  printf("Distance: %.4f\n", d / normlen);
}

const double *Plane::project(const double *dot) {
  // Project a dot onto this plane
  if (dim == 2) {
    return dot;
  }
  auto ret = new double[dim];
  auto fac = (dot_prod(dot, norm, dim) + d) / normsq;
  for (int i = 0; i < 3; ++i) {
    ret[i] = dot[i] - norm[i] * fac;
  }
  return ret;
}

inline double is_left(const double *P0, const double *P1, const double *P2) {
  return ((P1[0] - P0[0]) * (P2[1] - P0[1]) -
          (P2[0] - P0[0]) * (P1[1] - P0[1]));
}

int winding_number(const double *points, const double *dot,
                   const int num_pnts) {
  int wn = 0;
  for (int i = 0; i < num_pnts; ++i) {
    const int offset = 2 * i;
    const int next = (i == num_pnts - 1) ? 0 : offset + 2;
    if (points[offset + 1] <= dot[1]) {
      if (points[next + 1] > dot[1]) {
        if (is_left(points + offset, points + next, dot) > 0) {
          ++wn;
        }
      }
    } else {
      if (points[next + 1] <= dot[1]) {
        if (is_left(points + offset, points + next, dot) < 0) {
          --wn;
        }
      }
    }
  }
  return wn;
}

double line_segment_dot(const double *lp0, const double *lp1, const double *dot,
                        const int n) {
  // Calculate the distance between the line segment defined by two
  // points in line and a dot.
  double v[n], w[n];
  for (int i = 0; i < n; ++i) {
    v[i] = lp1[i] - lp0[i];
    w[i] = dot[i] - lp0[i];
  }

  auto c1 = dot_prod(w, v, n);
  if (c1 < 0) {
    return dot_dot(dot, lp0, n);
  }

  auto c2 = dot_prod(v, v, n);
  if (c2 <= c1) {
    return dot_dot(dot, lp1, n);
  }
  auto p = c1 / c2;
  for (int i = 0; i < n; ++i) {
    v[i] *= p;
    v[i] += lp0[i];
  }
  return dot_dot(v, dot, n);
}

double polygon_dot(const double *points, const double *dot, const int num_pnts,
                   const int dims, const bool check_planar) {
  // def polygon_dot(np.ndarray points,np.ndarray  dot, check_planar=True):
  if (num_pnts == 1) {
    return dot_dot(points, dot, dims);
  }
  if (num_pnts == 2) {
    return line_segment_dot(points, points + dims, dot, dims);
  }
  auto plane = Plane(points, points + dims, points + dims + dims, dims);

  if (check_planar) {
    // if len(points) > 3 and len(dot) > 2:
    //         # get an estimate of the length scales involved
    //         if not _is_planar(points, atol=0, rtol=1e-3):
    //             raise RuntimeError(f"Point of polygon are not in a plane!")
  }
  // Simple projection onto 2D-plane. Drop main component of orthogonal vector
  const double *pnts;
  const double *_dot;
  if (dims == 3) {
    auto tmp = new double[num_pnts * 2];
    double *nrm = plane.norm;
    int i0, i1;
    if (nrm[0] > nrm[1]) { // 1 is not largest
      if (nrm[0] > nrm[2]) {
        // 0 is largest
        i0 = 1;
        i1 = 2;
      } else {
        // 2 is largest
        i0 = 0;
        i1 = 1;
      }
    } else { // 0 is not largest
      if (nrm[1] > nrm[2]) {
        // 1 is largest
        i0 = 0;
        i1 = 2;
      } else {
        // 2 is largest
        i0 = 0;
        i1 = 1;
      }
    }
    for (int i = 0; i < num_pnts; ++i) {
      tmp[2 * i] = points[i * 3 + i0];
      tmp[2 * i + 1] = points[i * 3 + i1];
    }
    pnts = tmp;
    auto proj = plane.project(dot);
    tmp = new double[2];
    tmp[0] = proj[i0];
    tmp[1] = proj[i1];
    _dot = tmp;
    delete[] proj;
  } else if (dims == 2) {
    pnts = points;
    _dot = dot;
  } else {
    throw std::runtime_error("Unexpected number of dimension - only 2D and 3D "
                             "Vectors are supported.");
  }
  auto wn = winding_number(pnts, _dot, num_pnts);
  if (dims == 3) {
    delete[] _dot;
    delete[] pnts;
  }

  if (wn == 0) {
    double min =
        line_segment_dot(points + (num_pnts - 1) * dims, points, dot, dims);
    for (int i = 0; i < num_pnts - 1; ++i) {
      auto ptr = points + i * dims;
      double tmp = line_segment_dot(ptr, ptr + dims, dot, dims);
      if (tmp < min) {
        min = tmp;
      }
    }
    return min;
  }
  return plane.dist(dot);
}

PolyMesh::PolyMesh(const double *datax, const double *datay, int nx, int ny)
    : nx(nx), ny(ny), datax(datax), datay(datay),
      num_cells((nx - 1) * (ny - 1)) {
  bounds = new double[num_cells * 2 * 4];
  int pos = 0;
  for (int i = 0; i < nx - 1; ++i) {
    for (int j = 0; j < ny - 1; ++j) {
      int iin = i * ny + j;
      bounds[pos++] = datax[iin];
      bounds[pos++] = datay[iin];
      bounds[pos++] = datax[iin + 1];
      bounds[pos++] = datay[iin + 1];
      bounds[pos++] = datax[iin + ny+1];
      bounds[pos++] = datay[iin + ny+1];
      bounds[pos++] = datax[iin + ny];
      bounds[pos++] = datay[iin + ny];
    }
  }
  // printf("%d %d=%d\n",num_cells, num_cells*8, pos);
  // assert(num_cells * 8 == pos);
}

PolyMesh::~PolyMesh(){
  delete[] bounds;
}

int PolyMesh::find_cell(const double *dot, int guess) {
  if (guess >= 0) {
    for (int i = -1; i < 2; ++i) {
      for (int j = -1; j < 2; ++j) {
        int pos = guess + i + (ny -1) * j;
        if (pos >= 0 and pos < num_cells) {
          if (winding_number(bounds + pos * 8, dot, 4)) {
            return pos;
          }
        }
      }
    }
  }

  for (int pos = 0; pos < num_cells; ++pos) {
    if (winding_number(bounds + pos * 8, dot, 4)) {
      return pos;
    }
  }
  return -1;
}
