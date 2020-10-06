

class Plane {
public:
  Plane(double *p0, double *p1, double *p2, int n);
  ~Plane();
  double dist(double *dot);

private:
  // double * p0, * p1, * p2;
  const int dim;
  double *norm;
  double d;
  double normsq;
  double normlen;
};

double dot_dot(double*, double*, int);
