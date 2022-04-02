from imports import *

def find_edges_cv(image_cv, a, b):
    edges = cv.Canny(image_cv, a, b)
    return edges

def get_edges_x_and_y_arrays(edges_np):
    # this function should return an array of values where the edges are
    width = np.size(edges_np[1])
    # print("The width is %d"%width)
    x_array = np.empty((0, 1))
    y_array = np.empty((0, 1))
    y_errors = np.empty((0,1))
    for x_index in range(0, width):
        values = np.where(x_index == edges_np[1])
        if np.size(values) >= 2:
            y_values = edges_np[0][values]
            y_values = [y_values[0], y_values[-1]]
            y_array = np.append(y_array, np.mean(y_values))
            y_errors = np.append(y_errors, np.std(y_values))
            x_array = np.append(x_array, x_index)
            # print (x_array)
            # print (y_array)
    return x_array, y_array, y_errors

def makeCurveFromDifferenceImage(difference_image):
    edges_cv = find_edges_cv(difference_image, 100, 200)
    edges_np = np.where(edges_cv == 255)
    x_means, y_means, y_errors = get_edges_x_and_y_arrays(edges_np)
    return x_means,y_means, y_errors