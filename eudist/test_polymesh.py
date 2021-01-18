import numpy as np
import eudist
from test_point_plane import random_rotation


class Transform(object):
    def __init__(self, dims=2):
        self.rot = random_rotation(dims)
        self.dims = dims
        self.off1 = np.random.normal(scale=3, size=dims)
        self.off2 = np.random.normal(scale=3, size=dims)
        self.scale = np.random.lognormal()

    def __call__(self, p):
        # return p
        slc = slice(None), None
        shp = p.shape
        p = p.reshape(2, -1)
        p *= self.scale
        p += self.off1[slc]
        p = np.matmul(self.rot, p)
        p += self.off2[slc]
        p = p.reshape(shp)
        return p


def test_polymesh_1():
    nx = 5
    ny = 7
    x = np.arange(nx + 1)[:, None] * np.ones((nx + 1, ny + 1))
    y = np.arange(ny + 1)[None, :] * np.ones((nx + 1, ny + 1))
    mesh = np.array([x, y])  # .flatten(), y.flatten()])
    trans = Transform(2)
    mesh = trans(mesh)
    cx, cy = np.random.randint(nx), np.random.randint(ny)
    cell0 = np.array([[cx, cy], [cx, cy + 1.0], [cx + 1, cy + 1], [cx + 1, cy]]).T
    cellid = cx * ny + cy
    cell = trans(cell0)
    a = cell[:, 0]
    b = cell[:, 1] - a
    c = cell[:, 3] - a
    d = cell[:, 2] - a - b - c
    meshx, meshy = mesh
    mesh = eudist.PolyMesh(meshx, meshy)

    for _ in range(10):
        xx, xy = np.random.rand(2) * 1.5 - 0.25
        pos = a + b * xx + c * xy + xx * xy * d
        isin = 0 <= xx <= 1 and 0 <= xy <= 1
        try:
            assert (mesh.find_cell(pos) == cellid) == isin
        except AssertionError:
            print(mesh.find_cell(pos), cellid, cx, cy, nx, ny)
            import matplotlib.pyplot as plt

            print(meshx.shape)
            data = ((x == cx) & (y == cy)).astype(int)
            plt.pcolormesh(meshx, meshy, data)
            plt.scatter(pos[0], pos[1])
            plt.plot(cell[0], cell[1])
            plt.show()
            raise
