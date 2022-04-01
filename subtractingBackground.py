import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

init_poly_vals = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # for [amp, cen, wid]
exp_init_vals = [0, 0, 0, 0]
quad_init_vals = [0, 0, 0]
circle_init_vals = [100, 200, 300]
linear_init_vals = [-10, 400]


def linear_fit(x, a, b):
    return a * x + b


def polynomial_curve(x, a, b, c, d, e, f, g, h, i):
    return a * x ** 8 + b * x ** 7 + c * x ** 6 + d * x ** 5 + e * x ** 4 + f * x ** 3 + g * x ** 2 + h * x + i


def exponential_curve(x, a, b, c, d):
    return a * np.exp(b * x + c) + d


def quadratic_fit(x, a, b, c):
    return a * x ** 2 + b * x + c


def circle_fit(x, a, b, r):
    return -np.sqrt(r ** 2 - (x - a) ** 2) + b


def find_edges_cv(image_cv):
    edges = cv.Canny(image_cv, 50, 200)
    return edges


def get_edges_x_and_y_arrays(edges_np):
    # this function should return an array of values where the edges are
    width = np.size(edges_np[1])
    # print("The width is %d"%width)
    x_array = np.empty((0, 1))
    y_array = np.empty((0, 1))
    for x_index in range(0, width):
        values = np.where(x_index == edges_np[1])
        if np.size(values) >= 2:
            y_values = edges_np[0][values]
            y_values = [y_values[0], y_values[-1]]
            y_array = np.append(y_array, np.mean(y_values))
            x_array = np.append(x_array, x_index)
            # print (x_array)
            # print (y_array)
    return x_array, y_array


def plot_image(ax, img):
    ax.imshow(img, cmap='gray')


def ax_plot_scatter(ax, x_values, y_values, label):
    ax.scatter(x_values, y_values, s=4, label=label)


def ax_plot_fit(ax, model_name, best_vals_array, x_array):
    print(ax)
    print(model_name)
    print(best_vals_array)
    print(x_array)
    print(model_name(x_array, *best_vals_array))
    try:
        ax.plot(x_array, model_name(x_array, *best_vals_array), c='blue', linewidth=4.0, label=model_name.__name__)
    except:
        print("ax.plot not working")


def fit_image(image_cv, fit_name, fit_init_vals):
    edges_cv = find_edges_cv(image_cv)
    edges_numpy = np.where(edges_cv == 255)
    try:
        x_array, y_array = get_edges_x_and_y_arrays(edges_numpy)
    except:
        print("Could not get means")
    try:
        fit_params, covar_matrix = curve_fit(fit_name, x_array, y_array, p0=fit_init_vals)
    except:
        print("curvefit not working")
    # best_circ_vals, covar_circ = curve_fit(circle_fit, y_array, x_array, p0=circle_init_vals)
    return image_cv, edges_cv, edges_numpy, x_array, y_array, fit_name, fit_params


def find_edges(difference):
    return cv.Canny(difference, 100, 200)


def create_difference_image(image_name, background_name, crop_array):
    crop_top, crop_bottom, crop_left, crop_right = crop_array
    img = cv.imread(image_name, 0)
    bg = cv.imread(background_name, 0)
    img = img[crop_top:crop_bottom, crop_left:crop_right]
    bg = bg[crop_top:crop_bottom, crop_left:crop_right]
    difference = img - bg
    return img, bg, difference


def try_to_make_scatter(ax, edges, fit_name, fit_init_params):
    try:
        print("Fitting Image")
        image_cv, edges_cv, edges_numpy, x_array, y_array, fit_name, fit_params = fit_image(edges, fit_name,
                                                                                            fit_init_params)
        print("X array size is %f" % np.size(x_array))
        try:
            ax_plot_fit(ax, fit_name, fit_params, x_array)
            return fit_params
        except:
            print("ax_plot_fit isn't working")
    except:
        print("No fit")

def reduce_noise(image_cv, lowT,highT):
    width,height = np.shape(image_cv)
    for i in range(width):
        for j in range(height):
            if image_cv[i,j]>highT or image_cv[i,j]<lowT:
                image_cv[i, j] = 0
    return image_cv

def make_array_image_comparison_reference(image_name_array, background_name, crop_array):
    cols = 3
    rows = 3
    counter = 1
    initial_fitting_params = quad_init_vals
    curve_array=[]
    for image_name in image_name_array:
        print("Working on " + image_name)
        ax = plt.subplot(rows, cols, counter)
        img, bg, difference = create_difference_image(image_name, background_name,
                                                      crop_array)
        difference = reduce_noise(difference,100,200)
        print("finding edges...")
        try:
            edges_cv= find_edges_cv(difference)
            edges_numpy = np.where(edges_cv == 255)
            x_edges,y_edges = get_edges_x_and_y_arrays(edges_numpy)
            ax.scatter(x_edges,y_edges, label="Edges")
        except:
            print("Edges not found")
        plot_image(ax, difference)

        plt.title('Difference Image')

        initial_fitting_params = try_to_make_scatter(ax, edges_cv, quadratic_fit, initial_fitting_params)
        ax.legend()
        curve_array.append(initial_fitting_params[0])
        counter += 1

    plt.show()
    plt.plot(curve_array)
    plt.show()


background_name = "initial_curve_test/DSC_0069.JPG"
image_array = [
    "initial_curve_test/DSC_0062.JPG",
    "initial_curve_test/DSC_0063.JPG",
    "initial_curve_test/DSC_0064.JPG",
    "initial_curve_test/DSC_0065.JPG",
    "initial_curve_test/DSC_0066.JPG",
    "initial_curve_test/DSC_0067.JPG",
    "initial_curve_test/DSC_0068.JPG",

]
"""
]
"""
crop_top, crop_bottom = 500, 1250
crop_left, crop_right = 1500, 3000
crop_array = [crop_top, crop_bottom, crop_left, crop_right]
make_array_image_comparison_reference(image_array, background_name, crop_array)
