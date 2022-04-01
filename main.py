import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

init_poly_vals = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # for [amp, cen, wid]
exp_init_vals = [0, 0, 0, 0]
quad_init_vals = [0, 0, 0]
circle_init_vals = [100, 200, 300]


def polynomial_curve(x, a, b, c, d, e, f, g, h, i):
    return a * x ** 8 + b * x ** 7 + c * x ** 6 + d * x ** 5 + e * x ** 4 + f * x ** 3 + g * x ** 2 + h * x + i


def exponential_curve(x, a, b, c, d):
    return a * np.exp(b * x + c) + d


def quadratic_fit(x, a, b, c):
    return a * x ** 2 + b * x + c


def circle_fit(x, a, b, r):
    return -np.sqrt(r ** 2 - (x - a) ** 2) + b


def find_edges_cv(image_cv):
    edges = cv.Canny(image_cv, 100, 200)
    return edges


def get_edges_x_and_y_arrays(edges_np):
    x_array = np.empty((0, 1))
    y_array = np.empty((0, 1))
    for y_index in range(0, 256):
        values = np.where(y_index == edges_np[0])
        if np.size(values) >= 2:
            x_values = edges_np[1][values]
            x_values = [x_values[0], x_values[-1]]
            x_array = np.append(x_array, np.mean(x_values))
            y_array = np.append(y_array, y_index)
    return x_array, y_array


def plot_image(ax, img):
    ax.imshow(img, cmap='gray')


def ax_plot_scatter(ax, x_values, y_values, label):
    ax.scatter(x_values, y_values, s=4, label=label)


def ax_plot_fit(ax, model_name, best_vals_array, y_array):
    ax.plot(model_name(y_array, *best_vals_array), y_array, c='blue', linewidth=4.0, label=model_name)

def plot_all_fits(image_cv,edges_cv,edges_numpy,x_array,y_array,fit_name,fit_params):
    rows = 2
    columns = 3
    counter = 1
    ax = plt.subplot(rows, columns, counter)
    plot_image(ax, image_cv)
    plt.title("Image")
    counter += 1

    ax = plt.subplot(rows, columns, counter)
    plot_image(ax, edges_cv)
    plt.title("Edges")
    counter += 1

    ax = plt.subplot(rows, columns, counter)
    ax_plot_scatter(ax, edges_numpy[1], edges_numpy[0], "Scatter of Edges")
    ax.legend()
    ax.invert_yaxis()
    counter += 1

    ax = plt.subplot(rows, columns, counter)
    ax_plot_scatter(ax, edges_numpy[1], edges_numpy[0], "Scatter of Edges")
    ax_plot_scatter(ax, x_array, y_array, "Scatter of Mean edges")
    ax.invert_yaxis()
    ax.legend()
    plt.title("Mean x value points")

    ax = plt.subplot(235)

    ax_plot_scatter(ax, x_array, y_array, "Scatter of Mean Edges")
    ax_plot_fit(ax, fit_name, fit_params, y_array)
    plt.title("Quadratic fit")
    plt.legend()
    ax.invert_yaxis()

    ax = plt.subplot(236)
    plt.xlim([np.min(edges_numpy[1]), np.max(edges_numpy[1])])
    ax.imshow(image_cv, cmap='gray')
    ax_plot_fit(ax, fit_name, fit_params, y_array)
    ax.set_aspect('auto')
    plt.title("Fit compared to Image")
    plt.show()

def fit_image(image_cv,fit_name,fit_init_vals):

    edges_cv = find_edges_cv(image_cv)
    edges_numpy = np.where(edges_cv == 255)
    x_array, y_array = get_edges_x_and_y_arrays(edges_numpy)
    #best_poly_vals, covar_poly = curve_fit(polynomial_curve, y_array, x_array, p0=init_poly_vals)
    #best_exp_vals, covar_exp = curve_fit(exponential_curve, y_array, x_array, p0=exp_init_vals)
    fit_params, covar_quad = curve_fit(fit_name, y_array, x_array, p0=fit_init_vals)
    #best_circ_vals, covar_circ = curve_fit(circle_fit, y_array, x_array, p0=circle_init_vals)
    return image_cv,edges_cv,edges_numpy,x_array,y_array,fit_name,fit_params




original_image_file = 'black-screened.jpg'
black_img_cv = cv.imread(original_image_file, 0)

green_image_file = "green_screened_image.jpg"
img_green = cv.imread(green_image_file, 0)

#plot_all_fits(*fit_image(black_img_cv,quadratic_fit,quad_init_vals))

#plot_all_fits(*fit_image(img_green,quadratic_fit,quad_init_vals))

image_name = "C:\\Users\\ava7\OneDrive\\Desktop\\Magneto Morphs\\firstPhotos\\DSC_0042.JPG"
background_name = "C:\\Users\\ava7\OneDrive\\Desktop\\Magneto Morphs\\firstPhotos\\DSC_0054.JPG"
crop_top,crop_bottom=600,1600
crop_left,crop_right = 400,2400
img = cv.imread(image_name, 0)
bg = cv.imread(background_name, 0)
img = img[crop_top:crop_bottom, crop_left:crop_right]
bg = bg[crop_top:crop_bottom, crop_left:crop_right]
difference = img-bg

plot_all_fits(*fit_image(difference,quadratic_fit,quad_init_vals))

"""
ax = plt.subplot(111)
plt.title("Polynomial Fit")

ax.scatter(x_array, y_array, c='red')
ax.plot(polynomial_curve(y_array, *best_poly_vals), y_array, c='blue', linewidth=4.0)
ax.invert_yaxis()
residualsSquared = np.sum((polynomial_curve(y_array, *best_poly_vals) - y_array) ** 2)
ax.text(150, 0, "Squared Residuals %f"% residualsSquared )
plt.savefig("polyfit.png")
plt.show()

ax = plt.subplot(438)
plt.title("Exponential Fit")
ax.scatter(x_array, y_array, c='red')
ax.plot(exponential_curve(y_array, *best_exp_vals), y_array, c='green', linewidth=4.0)
ax.invert_yaxis()
ax = plt.subplot(111)
plt.title("Quadratic Fit")
ax.scatter(x_array, y_array, c='red')
ax.plot(quadratic_fit(y_array, *best_quad_vals), y_array, c='yellow', linewidth=4.0)
ax.invert_yaxis()
residualsSquared = np.sum((quadratic_fit(y_array, *best_quad_vals) - y_array) ** 2)
ax.text(150, 0, "Squared Residuals %f"% residualsSquared )
plt.savefig("quadfit.png")
plt.show()
"""
"""
ax = plt.subplot(4,3,10)
plt.title("Circle Fit")
ax.scatter(x_array, y_array, c='red')
ax.plot(circle_fit(y_array, *best_circ_vals), y_array, c='yellow', linewidth=4.0)
ax.invert_yaxis()
"""
"""
y_residuals = x_array - polynomial_curve(y_array, best_vals[0], best_vals[1], best_vals[2], best_vals[3], best_vals[4], best_vals[5])
plt.plot(y_residuals,y_array)
ax.invert_yaxis()
plt.title("Y Residuals")
"""

"""
plt.clf()
fig, ax = plt.subplots()
ax.scatter(x[1],x[0])
ax.invert_yaxis()
fig.suptitle('Points Extracted from edge array')
ax.set_xlabel("X Values")
ax.set_ylabel("Y Values")
plt.show()
"""
