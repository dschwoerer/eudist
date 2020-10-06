"""
Library for calculating euclidean distances.

    This file is part of eudist.

    eudist is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    eudist is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with eudist.  If not, see <https://www.gnu.org/licenses/>.

"""

import numpy as np


class Plane(object):
    def __init__(self, *, p0, p1=None, p2=None):
        """
        The plane is either defined by 3 points, a point and a normal
        vector, or a point and two span vectors.
        Only 3 points are currently supported.
        """
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.v0 = p1 - p0
        self.v1 = p2 - p0
        # [a, b, c] are the elements of norm
        self.norm = np.cross(self.v0, self.v1)
        self.d = -np.dot(self.norm, self.p0)

    def project(self, dot):
        """
        Project a dot onto this plane
        """
        if len(dot) == 2:
            return dot
        return dot - self.norm * (np.dot(dot, self.norm) + self.d) / (
            np.dot(self.norm, self.norm)
        )

    def dist(self, dot):
        return dist_plane_dot(self, dot)


def dist_plane_dot(plane, dot):
    if len(dot) == 2:
        return 0
    return np.abs(np.dot(dot, plane.norm) + plane.d) / np.sqrt(
        np.dot(plane.norm, plane.norm)
    )


def dist_dot_dot(p0, p1):
    """
    Distance between two points
    """
    dist = p0 - p1
    return np.sqrt(np.dot(dist, dist))


def dist_line_segment_dot(line, dot):
    """
    Calculate the distance between the line segment defined by two
    points in line and a dot. 
    """
    v = line[1] - line[0]
    w = dot - line[0]

    c1 = np.dot(w, v)
    if c1 <= 0:
        return dist_dot_dot(dot, line[0])

    c2 = np.dot(v, v)
    if c2 <= c1:
        return dist_dot_dot(dot, line[1])

    p = c1 / c2
    proj = line[0] + p * v
    return dist_dot_dot(proj, dot)


def winding_number(points, dot):
    """
    Calculate winding number.
    
    Based on https://geomalgorithms.com/a03-_inclusion.html
    by softSurfer and Dan Sunday
    """

    def is_left(p0, p1, p2):
        d1 = p1 - p0
        d2 = p2 - p0
        return (d1[0] * d2[1]) - (d2[0] * d1[1])

    # Winding number counter
    wn = 0
    for i in range(len(points)):
        # Use -1 to get periodic boundary conditions
        if points[i - 1][1] <= dot[1]:
            if points[i][1] > dot[1]:
                if is_left(points[i - 1], points[i], dot) > 0:
                    wn += 1
        else:
            if points[i][1] <= dot[1]:
                if is_left(points[i - 1], points[i], dot) < 0:
                    wn -= 1
    return wn


def is_planar(points, *, rtol=1e-3, atol=1e-8):
    # 3 points are alwys in a plane
    if len(points) < 4:
        return True
    # 2 Dimensions are always in a plane
    if len(points[0]) < 3:
        return True
    scale = dist_dot_dot(points[0], points[1]) + dist_dot_dot(points[0], points[2])
    scale /= 2
    plane = Plane(p0=points[0], p1=points[1], p2=points[2])
    for i in range(3, len(points)):
        if plane.dist(points[i]) > scale * 1e-3:
            return False
    return True


def dist_polygon_dot(points, dot, check_planar=True):
    if len(points) == 1:
        return dist_dot_dot(points[0], dot)
    elif len(points) == 2:
        return dist_line_segment_dot(points, dot)
    plane = Plane(p0=points[0], p1=points[1], p2=points[2])
    if check_planar:
        if len(points) > 3 and len(dot) > 2:
            # get an estimate of the length scales involved
            if not is_planar(points, atol=0, rtol=1e-3):
                raise RuntimeError(f"Point of polygon are not in a plane!")

    # Simple projection onto 2D-plane. Drop main component of orthogonal vector
    if len(dot) == 3:
        slcr = [0, 1, 2]
        slcr.pop(np.argmax(np.abs(plane.norm)))
    elif len(dot) == 2:
        slcr = slice(None)
    else:
        raise RuntimeError("Only 2D or 3D supported!")

    wn = winding_number([p[slcr] for p in points], plane.project(dot)[slcr])
    if wn == 0:
        return np.min(
            [
                dist_line_segment_dot([points[i - 1], points[i]], dot)
                for i in range(len(points))
            ]
        )
    return plane.dist(dot)
