from .point_plane import *


def test_plane_point1():
    p0 = np.array([0, 0, 0])
    p1 = np.array([1, 0, 0])
    p2 = np.array([0, 1, 0])
    pl = Plane(p0=p0, p1=p1, p2=p2)
    assert dist_plane_dot(pl, np.array([0, 0, 1])) == 1
    assert dist_plane_dot(pl, np.array([0, 1, 1])) == 1
    assert dist_plane_dot(pl, np.array([1, 0, 1])) == 1
    assert dist_plane_dot(pl, np.array([0, 0, 2])) == 2
    assert dist_plane_dot(pl, np.array([0, 0, 0])) == 0


def test_plane_point2():
    p0 = np.array([0, 0, 1])
    p1 = np.array([1, 0, 0])
    p2 = np.array([0, 1, 0])
    pl = Plane(p0=p0, p1=p1, p2=p2)
    assert dist_plane_dot(pl, np.array([0, 0, 1])) == 0

    assert np.isclose(dist_plane_dot(pl, np.array([0, 1, 1])), np.sqrt(1 / 3))
    assert np.isclose(dist_plane_dot(pl, np.array([1, 0, 1])), np.sqrt(1 / 3))
    assert np.isclose(dist_plane_dot(pl, np.array([0, 0, 0])), np.sqrt(1 / 3))


def test_plane_pint3():
    for i in range(100):
        ps = [
            np.array([0.0, 0, 0]),
            np.array([1.0, 0, 0]),
            np.array([0.0, 1, 0]),
            np.array([0.0, 0, 1]),
        ]

        ps[3][0:2] = np.random.normal(size=2)
        off1 = np.random.normal(scale=3, size=3)
        off2 = np.random.normal(scale=3, size=3)
        # trans = np.random.normal(scale=3, size=(3,3))
        trans = np.eye(3)
        for i, j in [[0, 1], [2, 0], [1, 2]]:
            rot = np.eye(3)
            phi = np.random.random() * np.pi * 2
            c = np.cos(phi)
            s = np.sin(phi)
            rot[i, i] = c
            rot[j, j] = c
            rot[i, j] = -s
            rot[j, 1] = s
            trans = np.matmul(trans, rot)
        eig = np.abs(np.linalg.eig(trans)[0])
        # matrix is singular
        if np.max(eig) / np.min(eig) > 1e6:
            continue
        for p in ps:
            p += off1
            p = np.matmul(trans, p)
            p += off2
        pl = Plane(p0=ps[0], p1=ps[1], p2=ps[2])
        assert np.isclose(dist_plane_dot(pl, ps[3]), 1)
