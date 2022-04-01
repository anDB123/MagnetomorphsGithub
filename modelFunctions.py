import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import scipy.stats

poly_init_vals = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # for [amp, cen, wid]
exp_init_vals = [1, 0, 0, 0]
quad_init_vals = [0, 0, 0]
circle_init_vals = [1000, 900, 200]
linear_init_vals = [0, 0]
two_lines_init_vals = [0, 0, 0, 0]


def quadratic_fit(x, a, b, c):
    return a * x ** 2 + b * x + c


def linear_fit(x, a, b):
    return a * x + b


def polynomial_curve(x, a, b, c, d, e, f, g, h, i):
    return a * x ** 8 + b * x ** 7 + c * x ** 6 + d * x ** 5 + e * x ** 4 + f * x ** 3 + g * x ** 2 + h * x + i


def exponential_curve(x, a, b, c, d):
    return a * np.exp(b * x + c) + d


def quadratic_fit(x, a, b, c):
    return a * x ** 2 + b * x + c


def upside_down_circle_fit(x, r, a, b):
    return -np.sqrt(r ** 2 - (x - a) ** 2) + b

def circle_fit(x, r, a, b):
    return np.sqrt(r ** 2 - (x - a) ** 2) + b - r

quad_array = (quadratic_fit, quad_init_vals, 0)

poly_array = (polynomial_curve, poly_init_vals)

exp_array = (exponential_curve, exp_init_vals)

linear_array = (linear_fit, linear_init_vals)

circle_array = (circle_fit, circle_init_vals)
