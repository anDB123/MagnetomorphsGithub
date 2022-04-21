import scipy.optimize

from imports import *

def modelTheCurve(x_values, y_values,a, b, init_params):
    x_edges, full_y_array, a, b, model_fitted_params = linear_curve_linear_fit(x_values, y_values, a, b, [circle_fit,init_params])
    return x_edges, full_y_array, a, b, model_fitted_params


def get_first_middle_last_arrays(x_edges, y_edges, a, b):
    split_point_a, split_point_b = np.argmax(x_edges > a), np.argmax(x_edges > b)
    return np.split(x_edges, [split_point_a, split_point_b]), np.split(y_edges, [split_point_a, split_point_b])


def fit_first_middle_last_curve(x_edges_array, y_edges_array, model_array):
    [first_x_edges, middle_x_edges, last_x_edges], [first_y_edges, middle_y_edges,
                                                    last_y_edges] = x_edges_array, y_edges_array

    first_linear_params, first_linear_covar = curve_fit(linear_array[0], first_x_edges, first_y_edges,
                                                        p0=linear_array[1])
    first_y_array = linear_fit(first_x_edges, *first_linear_params)

    middle_curve_params, middle_curve_covar = curve_fit(model_array[0], middle_x_edges, middle_y_edges, p0=model_array[1])
    middle_y_array = model_array[0](middle_x_edges, *middle_curve_params)

    last_linear_params, last_linear_covar = curve_fit(linear_array[0], last_x_edges, last_y_edges, p0=linear_array[1])
    last_y_array = linear_fit(last_x_edges, *last_linear_params)

    full_y_array = np.concatenate((first_y_array, middle_y_array, last_y_array), axis=0)
    return full_y_array, middle_curve_params


def linear_curve_linear_fit(x_edges, y_edges, a, b, embedded_model_array):
    full_y_array, model_fitted_params = fit_first_middle_last_curve(*get_first_middle_last_arrays(x_edges, y_edges, a, b), embedded_model_array)
    return x_edges, full_y_array, a, b, model_fitted_params
