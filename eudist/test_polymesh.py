import numpy as np
import eudist
from test_point_plane import random_rotation


class Transform(object):
    def __init__(self, dims=2):
        self.rot = random_rotation(dims)
        self.dims = dims
        self.off1 = np.random.normal(scale=3, size=dims)[:, None]
        self.off2 = np.random.normal(scale=3, size=dims)[:, None]
        self.scale = np.random.lognormal()

    def __call__(self, p):
        p *= self.scale
        p += self.off1
        p = np.matmul(self.rot, p)
        p += self.off2
        return p


def test_polymesh_1():
    nx = 5
    ny = 3
    x = np.arange(nx + 1)[:, None] * np.ones((nx + 1, ny + 1))
    y = np.arange(ny + 1)[None, :] * np.ones((nx + 1, ny + 1))
    mesh = np.array([x.flatten(), y.flatten()])
    trans = Transform(2)
    trans(mesh)
