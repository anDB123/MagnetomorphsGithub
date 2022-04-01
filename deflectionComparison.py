import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import scipy.stats

from edgeDetectionFunctions import *
from plottingFunctions import *
from modelFunctions import *

def estimate_errors(y_array):
    error_array = []
    min_error = 1
    for i in range(0, np.size(y_array)):
        if i == 0 or i == (np.size(y_array) - 1):
            error = 100
        else:
            error = (y_array[i - 1] + y_array[i] + y_array[i + 1]) / 3 - y_array[i]
        if error < min_error:
            error = min_error
        error_array.append(error)
    return error_array


def scipy_fit(fit_func, x_edges, y_edges, init_array):
    return curve_fit(fit_func, x_edges, y_edges, p0=init_array)


def find_reduced_chi_squared(observed, predicted, errors):
    return np.sum(((observed - predicted) ** 2 / errors) / (np.size(observed) - 1))


def linear_quad_linear_fit(x_edges, y_edges, a, b):
    # first linear fit
    first_x_edges = np.where((x_edges < a), x_edges)
    first_y_edges = np.where((x_edges < a), y_edges)
    first_linear_params, first_linear_covar = scipy_fit(linear_array[0], first_x_edges, first_y_edges, linear_array[1])
    # second linear fit
    last_x_edges = np.where((x_edges > b), x_edges)
    last_y_edges = np.where((x_edges > b), y_edges)
    last_linear_params, last_linear_covar = scipy_fit(linear_array[0], last_x_edges, last_y_edges, linear_array[1])
    # quadratic fits
    middle_x_edges = np.where((a <= x_edges <= b), x_edges)
    middle_y_edges = np.where((a <= x_edges <= b), y_edges)
    middle_linear_params, middle_linear_covar = scipy_fit(quad_array[0], middle_x_edges, middle_y_edges, quad_array[1])

    return first_linear_params, middle_linear_params, last_linear_params, first_x_edges, middle_x_edges, last_x_edges


def make_array_image_comparison_reference(image_array, background_name, crop_array, fit_array, x_values):
    cols = 3
    rows = 3
    counter = 1
    low_t = 100
    high_t = 170

    deflection_curves = []
    deflection_fits = []
    chi_squareds = []
    for image_name in image_array:
        print("Working on " + image_name)
        img, bg, difference = create_difference_image(image_name, background_name,
                                                      crop_array)
        ax = plt.subplot(rows, cols, counter)
        plt.xticks([])
        plt.yticks([])
        print("Reducing Noise...")
        low_noise_difference = reduce_noise(difference, low_t, high_t)
        plot_image(ax, low_noise_difference)
        print("finding edges...")
        edges_cv = find_edges_cv(low_noise_difference, 100, 200)
        edges_numpy = np.where(edges_cv == 255)
        x_edges, y_edges = get_edges_x_and_y_arrays(edges_numpy)
        ax.plot(x_edges, y_edges, label="Edges", linewidth=1, c='r')
        fit_params, covar_matrix = scipy_fit(fit_array[0], x_edges, y_edges, fit_array[1])
        ax.plot(x_edges, fit_array[0](x_edges, *fit_params))
        #chi_squared = scipy.stats.chisquare(f_obs=y_edges, f_exp=fit_array[0](x_edges, *fit_params))[0]
        errors = estimate_errors(y_edges)
        reduced_chi_squared = find_reduced_chi_squared(y_edges, fit_array[0](x_edges, *fit_params), errors)
        chi_squared_label = "Reduced Chi Squared = {:.2f}".format(reduced_chi_squared)
        print(chi_squared_label)
        plt.title(chi_squared_label)
        # plt.title("lowT = %d and highT = %d" % (low_T, high_T))
        deflection_curves.append([x_edges, y_edges])
        deflection_fits.append(fit_params)
        chi_squareds.append(chi_squared_label)
        counter += 1
    plt.show()
    ax = plt.subplot()

    for i in range(len(deflection_curves)):
        x, y = deflection_curves[i]
        deflection_fit = deflection_fits[i]
        ax.scatter(x, y, label=chi_squareds[i])
        ax.plot(x, fit_array[0](x, *deflection_fit), c='k')
    ax.invert_yaxis()
    plt.legend()
    plt.show()
    print(deflection_fits)
    curve_params = []
    for i in deflection_fits: curve_params.append(-i[0])
    plt.plot(x_values, curve_params)
    plt.xlabel("Current (A)")
    plt.ylabel("Deflection")
    plt.show()


background_name = "initial_curve_test/DSC_0069.JPG"
image_array = []
for i in range(0, 9): image_array.append("initial_curve_test/DSC_006{}.JPG".format(i))
crop_top, crop_bottom = 500, 1250
crop_left, crop_right = 500, 3000
crop_array = [crop_top, crop_bottom, crop_left, crop_right]

x_values = [
    0.000,
    0.512,
    0.999,
    1.506,
    2.030,
    2.499,
    2.997,
    3.508,
    3.975
]
make_array_image_comparison_reference(image_array, background_name, crop_array, quad_array, x_values)
make_array_image_comparison_reference(image_array, background_name, crop_array, poly_array, x_values)
# make_array_image_comparison_reference(image_array, background_name, crop_array, exp_array)
# make_array_image_comparison_reference(image_array, background_name, crop_array, linear_array)
# make_array_image_comparison_reference(image_array, background_name, crop_array, two_lines_array)


