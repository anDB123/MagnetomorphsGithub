from edgeDetectionFunctions import *
from deflectionCurveFitting.modelFunctions import *


def find_reduced_chi_squared(observed, predicted, errors):
    return np.sum(((observed - predicted) ** 2 / errors) / (np.size(observed) - 1))


def get_first_middle_last_arrays(x_edges, y_edges, a, b):
    split_point_a, split_point_b = np.argmax(x_edges > a), np.argmax(x_edges > b)
    return np.split(x_edges, [split_point_a, split_point_b]), np.split(y_edges, [split_point_a, split_point_b])


def fit_first_middle_last(x_edges_array, y_edges_array):
    [first_x_edges, middle_x_edges, last_x_edges], [first_y_edges, middle_y_edges,
                                                    last_y_edges] = x_edges_array, y_edges_array

    first_linear_params, first_linear_covar = curve_fit(linear_array[0], first_x_edges, first_y_edges,
                                                        p0=linear_array[1])
    first_y_array = linear_fit(first_x_edges, *first_linear_params)

    middle_quad_params, middle_quad_covar = curve_fit(quad_array[0], middle_x_edges, middle_y_edges, p0=quad_array[1])
    middle_y_array = quadratic_fit(middle_x_edges, *middle_quad_params)

    last_linear_params, last_linear_covar = curve_fit(linear_array[0], last_x_edges, last_y_edges, p0=linear_array[1])
    last_y_array = linear_fit(last_x_edges, *last_linear_params)

    full_y_array = np.concatenate((first_y_array, middle_y_array, last_y_array), axis=0)
    return full_y_array


def linear_quad_linear_fit(x_edges, y_edges, initial_a, initial_b):
    number_of_tests = 10  # higher will give better estimate (will take much longer though!!!)
    lower_limit = 0.1
    upper_limit = 1.6

    middle_of_lines = (initial_a + initial_b) / 2
    tested_a = np.linspace(initial_a * lower_limit, middle_of_lines, number_of_tests)
    tested_b = np.linspace(middle_of_lines, initial_b * upper_limit, number_of_tests)
    y_a_b_array = []
    red_chi_squared_array = []
    for a in tested_a:
        for b in tested_b:
            if a >= b:
                break
            full_y_array = fit_first_middle_last(*get_first_middle_last_arrays(x_edges, y_edges, a, b))
            y_errors = estimate_errors(y_edges)
            reduced_chi_squared = find_reduced_chi_squared(full_y_array, y_edges, y_errors)
            y_a_b_array.append([a, b])
            red_chi_squared_array.append(reduced_chi_squared)
    a, b = y_a_b_array[np.argmin(red_chi_squared_array)]
    print("final a = {}".format(a))
    print("final b = {}".format(b))
    full_y_array = fit_first_middle_last(*get_first_middle_last_arrays(x_edges, y_edges, a, b))
    return x_edges, full_y_array, a, b


def fit_first_middle_last_curve(x_edges_array, y_edges_array, model_array):
    [first_x_edges, middle_x_edges, last_x_edges], [first_y_edges, middle_y_edges,
                                                    last_y_edges] = x_edges_array, y_edges_array

    first_linear_params, first_linear_covar = curve_fit(linear_array[0], first_x_edges, first_y_edges,
                                                        p0=linear_array[1])
    first_y_array = linear_fit(first_x_edges, *first_linear_params)

    middle_curve_params, middle_curve_covar = curve_fit(model_array[0], middle_x_edges, middle_y_edges,
                                                        p0=model_array[1])
    middle_y_array = model_array[0](middle_x_edges, *middle_curve_params)

    last_linear_params, last_linear_covar = curve_fit(linear_array[0], last_x_edges, last_y_edges, p0=linear_array[1])
    last_y_array = linear_fit(last_x_edges, *last_linear_params)

    full_y_array = np.concatenate((first_y_array, middle_y_array, last_y_array), axis=0)
    return full_y_array, middle_curve_params


def linear_curve_linear_fit(x_edges, y_edges, a, b, embedded_model_array):
    full_y_array, model_fitted_params = fit_first_middle_last_curve(
        *get_first_middle_last_arrays(x_edges, y_edges, a, b), embedded_model_array)
    return x_edges, full_y_array, a, b, model_fitted_params


def get_edges(difference_cv):
    edges_cv = find_edges_cv(difference_cv, 100, 200)
    edges_numpy = np.where(edges_cv == 255)
    x_edges, y_edges = get_edges_x_and_y_arrays(edges_numpy)
    y_edges_error = estimate_errors(y_edges)
    return x_edges, y_edges, y_edges_error


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
