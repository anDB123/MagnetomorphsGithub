from imports import *


def get_edges_x_and_y_arrays(edges_np):
    # this function should return an array of values where the edges are
    width = np.size(edges_np[1])
    # print("The width is %d"%width)
    x_array = np.empty((0, 1))
    y_array = np.empty((0, 1))
    y_errors = np.empty((0, 1))
    for x_index in range(0, width):
        values = np.where(x_index == edges_np[1])
        if np.size(values) >= 2:
            y_values = edges_np[0][values]
            y_values = [y_values[0], y_values[-1]]
            y_array = np.append(y_array, np.max(y_values))
            x_array = np.append(x_array, x_index)
    min_error = 5
    err_range = 5
    for i in range(len(y_array)):
        if i <= err_range or i >= (len(y_array) + err_range):
            temp_err = min_error
        else:
            temp_err = (np.std(y_array[i - err_range:i + err_range]))
            if temp_err < min_error:
                temp_err = min_error
        y_errors = np.append(y_errors, temp_err)

    return x_array, y_array, y_errors


def makeCurveFromDifferenceImage(difference_image, a, b, aperture_size):
    edges_cv = cv.Canny(difference_image, a, b, aperture_size)
    edges_np = np.where(edges_cv == 255)
    x_means, y_means, y_errors = get_edges_x_and_y_arrays(edges_np)
    return x_means, y_means, y_errors
