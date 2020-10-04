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
        The plane is either defined by 3 points, a point and a normal vector, or a point and two span vectors.
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


def dist_plane_dot(plane, dot):
    return np.abs(np.dot(dot, plane.norm) + plane.d) / np.sqrt(
        np.dot(plane.norm, plane.norm)
    )
