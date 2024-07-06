import pytest
from geometry import Matrix, Vec3


def test_must_create_correct_matrix():
    m = Matrix()
    assert m.m() == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    m = Matrix(*range(1, 10))
    assert m.m() == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    m = Matrix(*range(1, 17), size=4)
    assert m.m() == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]

    m = Matrix(*range(1, 17), size=3)
    assert m.m() == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def test_matrix_must_subscript_correctly():
    m = Matrix(*range(1, 10))
    assert m[0] == [1, 2, 3]
    assert m[1] == [4, 5, 6]
    assert m[2] == [7, 8, 9]

    assert m[0, 0] == 1
    assert m[0, 1] == 2
    assert m[0, 2] == 3
    assert m[1, 0] == 4
    assert m[1, 1] == 5
    assert m[1, 2] == 6
    assert m[2, 0] == 7
    assert m[2, 1] == 8
    assert m[2, 2] == 9


@pytest.mark.parametrize('index', [3, (0, 3), (0, 0, 0), [], (1,), tuple()])
def test_matrix_must_raise_if_invalid_subscript(index):
    m = Matrix(*range(1, 10))

    with pytest.raises(IndexError):
        m[index]


def test_matrix_must_be_mutable_by_subscript():
    m = Matrix()

    m[0, 0] = -9
    m[0, 1] = -8
    m[0, 2] = -7
    m[1, 0] = -6
    m[1, 1] = -5
    m[1, 2] = -4
    m[2, 0] = -3
    m[2, 1] = -2
    m[2, 2] = -1
    assert m.m() == [[-9, -8, -7], [-6, -5, -4], [-3, -2, -1]]

    m[0] = [1, 2, 3]
    m[1] = [4, 5, 6]
    m[2] = [7, 8, 9]
    assert m.m() == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def test_matrix_must_be_equality_comparable():
    m1 = Matrix(*range(1, 10))
    m2 = Matrix(*range(1, 10))
    assert m1 == m2

    m1[0, 0] = -1
    assert m1 != m2


def test_matrix_must_multiply_correctly():
    m1 = Matrix(*range(1, 10))
    m2 = Matrix(*range(10, 100, 10))
    m3 = m1 * m2
    assert m3.m() == [[1 * 10 + 2 * 40 + 3 * 70, 1 * 20 + 2 * 50 + 3 * 80, 1 * 30 + 2 * 60 + 3 * 90],
                      [4 * 10 + 5 * 40 + 6 * 70, 4 * 20 + 5 * 50 + 6 * 80, 4 * 30 + 5 * 60 + 6 * 90],
                      [7 * 10 + 8 * 40 + 9 * 70, 7 * 20 + 8 * 50 + 9 * 80, 7 * 30 + 8 * 60 + 9 * 90]]


    m3 = m2 * m1

    v = Vec3(10, 20, 30)
    v1 = m1 * v
    assert (v1.x, v1.y, v1.z) == (1 * 10 + 2 * 20 + 3 * 30, 4 * 10 + 5 * 20 + 6 * 30, 7 * 10 + 8 * 20 + 9 * 30)