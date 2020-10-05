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


def random_rotation(dims):
    if dims == 3:
        trans = np.eye(3)
        for i, j in [[0, 1], [0, 2], [1, 2]]:
            rot = np.eye(3)
            phi = np.random.random() * np.pi * 2
            c = np.cos(phi)
            s = np.sin(phi)
            rot[i, i] = c
            rot[j, j] = c
            rot[i, j] = -s
            rot[j, i] = s
            trans = np.matmul(trans, rot)
        eig = np.abs(np.linalg.eig(trans)[0])
        # matrix is singular
        # print(np.max(eig), np.min(eig))
        if np.max(eig) / np.min(eig) > 1 + dims * 1e-6:
            raise RuntimeError("Roational matrix should have eigenvalue 1!")
        return trans
    elif dims == 2:
        phi = np.random.random() * np.pi * 2
        c = np.cos(phi)
        s = np.sin(phi)
        rot = np.array([[c, -s], [s, c]])
        return rot
    elif dims > 3:
        trans = np.eye(dims)
        for i in range(dims):
            for j in range(i):
                rot = np.eye(dims)
                phi = np.random.random() * np.pi * 2
                c = np.cos(phi)
                s = np.sin(phi)
                rot[i, i] = c
                rot[j, j] = c
                rot[i, j] = -s
                rot[j, i] = s
                trans = np.matmul(trans, rot)
        eig = np.abs(np.linalg.eig(trans)[0])
        if np.max(eig) / np.min(eig) > 1 + dims * 1e-6:
            raise RuntimeError("Roational matrix should have eigenvalue 1!")
        return trans
    raise RuntimeError(f"not implemented for dim={dims}")


def test_plane_point3():
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
        trans = random_rotation(dims=3)
        for p in ps:
            p += off1
            p = np.matmul(trans, p)
            p += off2
        pl = Plane(p0=ps[0], p1=ps[1], p2=ps[2])
        assert np.isclose(dist_plane_dot(pl, ps[3]), 1)


def test_dist_dot_dot():
    for i in range(100):
        for n in [1, 2, 3, 5, 8]:
            p0 = np.random.normal(scale=3, size=n)
            p1 = np.random.normal(scale=3, size=n)
            assert np.isclose(dist_dot_dot(p0, p1), np.sqrt(np.dot(p0 - p1, p0 - p1)))
    for i in range(100):
        n = 3
        rotate = random_rotation(n)
        p0 = np.zeros(n)
        p1 = np.zeros(n)
        p0[0] = 1
        p1[0] = 2
        p0 = p0 @ rotate
        p1 = p1 @ rotate
        assert np.isclose(dist_dot_dot(p0, p1), 1)
    p0 = np.array([1, 0, 0])
    p1 = np.array([2, 0, 0])
    assert np.isclose(dist_dot_dot(p0, p1), 1)
    p1 = np.array([0, 0, 0])
    assert np.isclose(dist_dot_dot(p0, p1), 1)
    p0 = np.array([1])
    p1 = np.array([2])
    assert np.isclose(dist_dot_dot(p0, p1), 1)
    p0 = np.array([1, 1, 1])
    p1 = np.array([2, 2, 2])
    assert np.isclose(dist_dot_dot(p0, p1), np.sqrt(3))


def test_winding_number():
    for i in range(100):
        n = 2
        pnts = np.zeros((4, n))
        pnts[1, 0] = 1
        pnts[2, 0] = 1
        pnts[2, 1] = 1
        pnts[3, 1] = 1
        dot = np.random.normal(scale=3, size=n)
        expected = 0
        if 0 <= dot[0] <= 1 and 0 <= dot[1] <= 1:
            expected = 1
        rot = random_rotation(2)
        scal = np.random.lognormal()
        trans = rot * scal
        pnts = pnts @ trans
        dot = dot @ trans

        wn = winding_number(pnts, dot)
        assert wn == expected
