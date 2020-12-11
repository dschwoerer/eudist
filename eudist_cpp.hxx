

class Plane {
public:
  Plane(const double *p0, const double *p1, const double *p2, int n);
  ~Plane();
  double dist(const double *dot);
  double signed_dist(const double *dot);
  const double *project(const double *dot);
  double *norm;
  void info();

private:
  // double * p0, * p1, * p2;
  const int dim;
  double d;
  double normsq;
  double normlen;
};

double dot_dot(const double *, const double *, int);

int winding_number(const double *, const double *, int);

double polygon_dot(const double *, const double *, int, int, bool);

class PolyMesh {
public:
  PolyMesh(const double *datax, const double *datay, int nx, int ny);
  ~PolyMesh();

  int find_cell(const double *dot, int guess);

private:
  const int nx;
  const int ny;
  const double *datax;
  const double *datay;
  const int num_cells;
  double *bounds;
};
