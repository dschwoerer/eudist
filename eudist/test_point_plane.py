from eudist import *


def test_plane_point1():
    p0 = np.array([0.0, 0, 0], dtype=float)
    p1 = np.array([1.0, 0, 0], dtype=float)
    p2 = np.array([0.0, 1, 0], dtype=float)
    pl = Plane(p0=p0, p1=p1, p2=p2)
    for pnt, val in [
        (np.array([0.0, 0, 1]), 1),
        (np.array([0.0, 1, 1]), 1),
        (np.array([1.0, 0, 1]), 1),
        (np.array([0.0, 0, 2]), 2),
        (np.array([0.0, 0, 0]), 0),
    ]:
        assert plane_dot(pl, pnt) == val
        assert pl.dist(pnt) == val


def test_plane_point2():
    p0 = np.array([0.0, 0, 1], dtype=float)
    p1 = np.array([1.0, 0, 0], dtype=float)
    p2 = np.array([0.0, 1, 0], dtype=float)
    pl = Plane(p0=p0, p1=p1, p2=p2)
    assert plane_dot(pl, np.array([0.0, 0, 1])) == 0
    assert np.isclose(plane_dot(pl, np.array([0.0, 1, 1])), np.sqrt(1 / 3))
    assert np.isclose(plane_dot(pl, np.array([1.0, 0, 1])), np.sqrt(1 / 3))
    assert np.isclose(plane_dot(pl, np.array([0.0, 0, 0])), np.sqrt(1 / 3))


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
        dist = 3
        ps = [
            np.array([0.0, 0, 0]),
            np.array([1.0, 0, 0]),
            np.array([0.0, 1, 0]),
            np.array([0.0, 0, dist]),
        ]

        ps[3][0:2] = np.random.normal(size=2)
        off1 = np.random.normal(scale=3, size=3)
        off2 = np.random.normal(scale=3, size=3)
        trans = random_rotation(dims=3)
        scal = np.random.lognormal()
        dist *= scal
        for p in ps:
            p *= scal
            p += off1
            p = np.matmul(trans, p)
            p += off2
        pl = Plane(p0=ps[0], p1=ps[1], p2=ps[2])
        assert np.isclose(plane_dot(pl, ps[3]), dist)
        assert np.isclose(pl.dist(ps[3]), dist)


def test_plane_point4():
    for i in range(100):
        ps = np.random.random((4, 3))
        ps[:3, 0] = 0
        dist = ps[3, 0]
        ps = [p for p in ps]
        off1 = np.random.normal(scale=3, size=3)
        off2 = np.random.normal(scale=3, size=3)
        trans = random_rotation(dims=3)
        scal = np.random.lognormal()
        dist *= scal
        for p in ps:
            p *= scal
            p += off1
            p = np.matmul(trans, p)
            p += off2
        pl = Plane(p0=ps[0], p1=ps[1], p2=ps[2])
        assert np.isclose(plane_dot(pl, ps[3]), dist)
        assert np.isclose(pl.dist(ps[3]), dist)


def test_plane_point5():
    ps = np.array(
        [
            [5.45458, 0.0, -0.374516],
            [5.47951, 0.0, -0.383842],
            [5.48446459, 0.01914447, -0.383323],
            [5.45953074, 0.01905743, -0.374144],
        ]
    )
    # ps = [p for p in ps]
    pl = Plane(p0=ps[0], p1=ps[1], p2=ps[2])
    assert pl.dist(ps[3]) < 1
    assert Plane(p0=ps[0], p1=ps[1], p2=ps[2]).dist(ps[3]) < 0.01


def test_dot_dot():
    for i in range(100):
        for n in [1, 2, 3, 5, 8]:
            p0 = np.random.normal(scale=3, size=n)
            p1 = np.random.normal(scale=3, size=n)
            assert np.isclose(dot_dot(p0, p1), np.sqrt(np.dot(p0 - p1, p0 - p1)))
    for i in range(100):
        n = 3
        rotate = random_rotation(n)
        p0 = np.zeros(n)
        p1 = np.zeros(n)
        p0[0] = 1
        p1[0] = 2
        p0 = p0 @ rotate
        p1 = p1 @ rotate
        assert np.isclose(dot_dot(p0, p1), 1)
    p0 = np.array([1.0, 0, 0])
    p1 = np.array([2.0, 0, 0])
    assert np.isclose(dot_dot(p0, p1), 1)
    p1 = np.array([0.0, 0, 0])
    assert np.isclose(dot_dot(p0, p1), 1)
    p0 = np.array([1.0])
    p1 = np.array([2.0])
    assert np.isclose(dot_dot(p0, p1), 1)
    p0 = np.array([1.0, 1, 1])
    p1 = np.array([2.0, 2, 2])
    assert np.isclose(dot_dot(p0, p1), np.sqrt(3))


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


def test_polygone_dot():
    for i in range(1000):
        n = 3
        # make a square
        pnts = np.zeros((4, n))
        pnts[1, 0] = 1
        pnts[2, 0] = 1
        pnts[2, 1] = 1
        pnts[3, 1] = 1
        pnts[:, :2] -= 0.5
        # A random dot
        dot = np.random.normal(scale=3, size=n)
        # dot = np.array([.4,.2,1])
        # Calculate distance
        dist = np.abs(dot)
        for i in range(2):
            dist[i] -= 0.5
            if dist[i] < 0:
                dist[i] = 0
        dist = np.sqrt(np.dot(dist, dist))
        # Add some offset
        offset = np.random.normal(scale=3, size=n)
        pnts += offset
        dot += offset

        # Rotate and scale
        rot = random_rotation(n)
        scal = np.random.lognormal()
        dist *= scal
        trans = rot * scal
        pnts = pnts @ trans
        dot = dot @ trans

        calc = polygon_dot(pnts, dot)
        if not np.isclose(dist, calc):
            import matplotlib.pyplot as plt

            for i in range(n):
                for j in range(i):
                    plt.figure()
                    plt.plot(pnts[:, i], pnts[:, j], "-o")
                    plt.plot(dot[i], dot[j], "x")
            plt.show()
            raise AssertionError


if __name__ == "__main__":
    test_plane_point1()
    test_plane_point2()
    test_plane_point3()
    test_plane_point4()
    test_dot_dot()
    test_winding_number()
    test_polygone_dot()
