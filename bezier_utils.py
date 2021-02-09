import numpy as np
from scipy.special import comb
from sympy import *

t = symbols('t')
number_of_points = 20


def get_blending(i, n):
    return comb(n, i, exact=True) * pow(1 - t, n - i) * pow(t, i)


def get_bezier_curve(points):
    bezier_curve = np.array([0, 0])

    for i in range(len(points)):
        bezier_curve = np.add(bezier_curve, np.dot(points[i], get_blending(i, len(points) - 1)))

    return bezier_curve


def get_bezier_points(points):
    bezier_curve = get_bezier_curve(points)
    bezier_points = []

    if len(points) != 0:
        for i in np.arange(0, 1, 1 / number_of_points):
            bezier_points.append([bezier_curve[0].subs(t, i), bezier_curve[1].subs(t, i)])

    return bezier_points
