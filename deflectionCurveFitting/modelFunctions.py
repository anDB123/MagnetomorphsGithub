from imports import *

quad_init_vals = [0, 0, 0]
def quadratic_fit(x, a, b, c):
    return a * x ** 2 + b * x + c
quad_array = (quadratic_fit, quad_init_vals)

linear_init_vals = [0, 0]
def linear_fit(x, a, b):
    return a * x + b
linear_array = (linear_fit, linear_init_vals)

poly_init_vals = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # for [amp, cen, wid]
def polynomial_curve(x, a, b, c, d, e, f, g, h, i):
    return a * x ** 8 + b * x ** 7 + c * x ** 6 + d * x ** 5 + e * x ** 4 + f * x ** 3 + g * x ** 2 + h * x + i
poly_array = (polynomial_curve, poly_init_vals)

exp_init_vals = [1, 0, 0, 0]
def exponential_curve(x, a, b, c, d):
    return a * np.exp(b * x + c) + d
exp_array = (exponential_curve, exp_init_vals)

upside_down_circle_init_vals = [1000, 900, 200]
def upside_down_circle_fit(x, r, a, b):
    return np.sqrt(r ** 2 - (x - a) ** 2) - (b - r)

circle_init_vals = [1000, 900, 200]
def circle_fit(x, r, a, b):
    return np.sqrt(r ** 2 - (x - a) ** 2) + b - r
circle_array = (circle_fit, circle_init_vals)