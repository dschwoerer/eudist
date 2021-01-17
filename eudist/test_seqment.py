import eudist as eudist
import numpy as np


def random_rotation(dims):
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


def dotestseqseq(a, b, *, iter=100, expect=True):
    assert eudist.do_seg_seg_intersect(a, b) == expect
    a0 = a
    b0 = b
    for i in range(iter):
        a = a0.copy()
        b = b0.copy()
        off1 = np.random.normal(scale=3, size=2)
        off2 = np.random.normal(scale=3, size=2)
        trans = random_rotation(dims=2)
        scal = np.random.lognormal()
        for p in [a, b]:
            p *= scal
            p += off1
            p = np.matmul(trans, p)
            p += off2
        assert eudist.do_seg_seg_intersect(a, b) == expect


def test_seq_seq0():
    a = np.zeros((2, 2))
    b = np.zeros((2, 2))
    a[0, 1] = 1
    a[1, 1] = -1
    b[0, 0] = 1
    b[1, 0] = -1
    dotestseqseq(a, b)
    dotestseqseq(b, a)


test_seq_seq0()


def test_seq_seq1():
    a = np.zeros((2, 2))
    b = np.zeros((2, 2))
    a[0, 1] = 1
    b[1, 0] = 1
    dotestseqseq(a, b)
    dotestseqseq(b, a)


test_seq_seq1()


def test_seq_seq2():
    A = [[0.0, 0], [3, 3]]
    B = [[-2.0, 2], [2, -2]]
    for _ in range(10):
        a = np.array(A)
        b = np.array(B)
        off = np.random.random(1) * 5

        dotestseqseq(a, b + off, iter=10, expect=(off < 3))


def test_seq_seq3():
    for i in [1, -1]:
        for j in [1, -1]:
            a = np.array([[0.0, 0], [0, 1]])[::i]
            b = np.array([[0.0, 0], [1, 0]])[::j]
            dotestseqseq(a, b, iter=10)


# def test_parallel():
#     a = np.array([[0.0, 0], [0, 1]])
#     for i in range(10):
#         b = a.copy()
#         off = np.random.random(1) * 2
#         b[:, 1] += off
#         dotestseqseq(a, b, iter=10, expect=(off < 1))

# def test_seq_seq4():
#     a = np.array([[0.0, 0], [0, 1]])
#     for i in range(10):
#         b = np.array([[0.0, 0], [0, 1]])
#         off = np.random.random(1) * 2
#         b[:, 1] += off
#         dotestseqseq(a, b, iter=10, expect=(off < 1))
