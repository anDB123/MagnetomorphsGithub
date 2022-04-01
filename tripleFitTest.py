import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import scipy.stats
import math

from edgeDetectionFunctions import *
from plottingFunctions import *
from modelFunctions import *
from fitting_code import *


def make_array_image_comparison_reference(image_array, background_name, crop_array, x_values, model, model_init_params):
    # function to generate difference image, find edges, find centre between edges, model centres and plot the result
    cols = 3
    rows = math.ceil(len(image_array) / cols)
    counter = 1
    low_t, high_t = 100, 170
    initial_a, initial_b = 1100.0, 1600.0
    deflection_curves,deflection_fits,chi_squareds = [],[],[]
    for image_name in image_array:
        # Keeping track of progress
        print("Working on " + image_name)
        # using open cv to make image arrays
        img, bg, difference = create_difference_image(image_name, background_name, crop_array)
        # noise reduction on image
        low_noise_difference = reduce_noise(difference, low_t, high_t)
        # finding edges
        x_edges, y_edges, y_edges_error = get_edges(low_noise_difference)
        # fitting
        x_model_array, y_model_array, a, b = model(x_edges, y_edges, *model_init_params)
        # find reduced chi squared
        reduced_chi_squared = find_reduced_chi_squared(y_edges, y_model_array, y_edges_error)
        chi_squared_label = "I = {}A, $\chi_r^2$ = {:.2f}".format(x_values[counter - 1], reduced_chi_squared)
        # Plotting
        ax = plt.subplot(rows, cols, counter)
        plot_image_with_fit(ax,low_noise_difference,x_edges,y_edges,x_model_array,y_model_array,chi_squared_label,a,b)
        # appending arrays
        deflection_curves.append([x_edges, y_edges])
        deflection_fits.append([x_model_array, y_model_array])
        chi_squareds.append(chi_squared_label)
        counter += 1
    plt.tight_layout()
    plt.show()
    # making new subplot
    ax = plt.subplot()
    for i in range(len(deflection_curves)):
        # making deflection curves with the modelled fit
        x, y = deflection_curves[i]
        model_x, model_y = deflection_fits[i]
        ax.scatter(x, y, label=chi_squareds[i])
        ax.plot(model_x, model_y, c='k')
    ax.invert_yaxis()
    plt.legend()

    plt.show()


background_name = "initial_curve_test/DSC_0069.JPG"
image_array = []
for i in range(0, 9): image_array.append("initial_curve_test/DSC_006{}.JPG".format(i))
crop_top, crop_bottom = 500, 1250
crop_left, crop_right = 0, 3000
crop_array = [crop_top, crop_bottom, crop_left, crop_right]
x_values = [0.000, 0.512, 0.999, 1.506, 2.030, 2.499, 2.997, 3.508, 3.975]
model = linear_quad_linear_fit
model_init_params = 1100.0, 1600.0
make_array_image_comparison_reference(image_array, background_name, crop_array, x_values, model, model_init_params)
"""
background_name = "red_background_curve_test/DSC_0114.JPG"
"""