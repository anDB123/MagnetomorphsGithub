import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import scipy.stats

from edgeDetectionFunctions import *
from plottingFunctions import *
from modelFunctions import *



def find_reduced_chi_squared(observed, predicted, errors):
    return np.sum(((observed - predicted) ** 2 / errors) / (np.size(observed) - 1))


def scipy_fit(fit_func, x_edges, y_edges, init_array):
    return curve_fit(fit_func, x_edges, y_edges, p0=init_array)

def linear_quad_linear_fit(x_edges, y_edges, initial_a, initial_b):
    # first linear fit
    print("a = {}".format(a))
    print("b = {}".format(b))
    number_of_tests = 100
    lower_limit = 0.5
    upper_limit = 1.5
    tested_a = np.linspace(initial_a * lower_limit, initial_a * upper_limit, number_of_tests)
    tested_b = np.linspace(initial_b * lower_limit, initial_b * upper_limit, number_of_tests)
    for a in tested_a:
        for b in tested_b:
            try:
                first_x_edges = np.where((x_edges < a), x_edges, np.nan)
                first_x_edges = first_x_edges[~np.isnan(first_x_edges)]

                first_y_edges = np.where((x_edges < a), y_edges, np.nan)
                first_y_edges = first_y_edges[~np.isnan(first_y_edges)]

                first_linear_params, first_linear_covar = scipy_fit(linear_array[0], first_x_edges, first_y_edges, linear_array[1])
                first_y_array = linear_fit(first_x_edges, *first_linear_params)
                # second linear fit
                last_x_edges = np.where((x_edges > b), x_edges, np.nan)
                last_y_edges = np.where((x_edges > b), y_edges, np.nan)

                last_x_edges = last_x_edges[~np.isnan(last_x_edges)]
                last_y_edges = last_y_edges[~np.isnan(last_y_edges)]

                last_linear_params, last_linear_covar = scipy_fit(linear_array[0], last_x_edges, last_y_edges, linear_array[1])
                last_y_array = linear_fit(last_x_edges, *last_linear_params)
                # quadratic fit
                try:

                    middle_x_edges = np.where((a <= x_edges), x_edges, np.nan)
                    middle_x_edges = np.where((b >= x_edges), middle_x_edges, np.nan)
                    middle_y_edges = np.where((a <= x_edges), y_edges, np.nan)
                    middle_y_edges = np.where((b >= x_edges), middle_y_edges, np.nan)
                except:
                    print("Middle edges not working")
                try:
                    middle_x_edges = middle_x_edges[~np.isnan(middle_x_edges)]
                    middle_y_edges = middle_y_edges[~np.isnan(middle_y_edges)]
                except:
                    print("Nan removal not working")
                try:
                    middle_quad_params, middle_quad_covar = scipy_fit(quad_array[0], middle_x_edges, middle_y_edges,
                                                                      quad_array[1])
                except:
                    print("Not able to get a good quadratic fit")
                middle_y_array = quadratic_fit(middle_x_edges, *middle_quad_params)
                full_y_array = np.concatenate((first_y_array, middle_y_array, last_y_array), axis=0)
                reduced_chi_squared = find_reduced_chi_squared(full_y_array,y_edges,y_edges/100)
                print("reduced chi squared = {}".format(reduced_chi_squared))
            except:
                print("Fit didn't work")
    return x_edges, full_y_array,a,b

x1= np.linspace(0,10,100)
x2= np.linspace(10,20,100)
x3= np.linspace(20,30,100)
y1=40*x1 + 3
y2 = 10*x2**2 - 200*x2 + 400
y3= -40*x3 + 3

x= np.concatenate((x1,x2,x3),axis=0)
y= np.concatenate((y1,y2,y3),axis=0)
plt.plot(x,y)
plt.show()

linear_quad_linear_fit()