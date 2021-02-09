import numpy as np


def get_knot_vector(k, n):
    return [i for i in np.arange(0, 1 + 1 / (k + n + 1), 1 / (k + n + 1))]


def get_n(i, j, t):
    if j == 0:
        if i <= t < i + 1:
            return 1
        else:
            return 0

    return ((t - i) * get_n(i, j - 1, t) / j) + ((i + j + 1 - t) * get_n(i + 1, j - 1, t) / j)


def get_point(k, t, points):
    point = np.array([0, 0])

    count = 0
    for tmp_point in points:
        cox = get_n(count, k, t)
        point = point + cox * tmp_point
        count = count + 1

    return point


def get_b_spline_points(k, points):
    curve_points = []

    if len(points) > k:
        for t in np.arange(k, len(points), 1 / 100):
            point = get_point(k, t, points)

            curve_points.append(point)

    return curve_points
