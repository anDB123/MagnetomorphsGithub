import matplotlib.pyplot as plt
import numpy as np

from imports import *

testNoiseReduction = False
testCropping = False
makingGrid = True
makingCurveComparison = True
showFirstImageIndividually = False
testHSVNoiseReduction = False

graph_dir = "C:/Users/AndyPC/Desktop/MagnetomorphsGithub/graphs"

image_array = ["../29redBackground/DSC_00{} (3).JPG".format(i) for i in range(59, 68)]
bg_image = "../29redBackground/DSC_0068 (3).JPG"
"""

image_array = ["../betterContrast/DSC_00{}.JPG".format(i) for i in range(21, 60)]
bg_image = "../betterContrast/DSC_0061.JPG"
"""
currents_array = np.linspace(0, 4, 9)

crop_29 = [100, 1000, 300, 2800]
blue_only_noise_reduction = [101, 210]

any_colour_noise_reduction_array = [[0, 255], [0, 255], [100, 200]]
thickness = 2
number_of_curves = 30

init_vals = [10000, 0, 0]
circle_bounds = [[1, 0, 0], [np.inf, np.inf, np.inf]]
curve_params = [circle_fit, init_vals, circle_bounds]

initial_difference_image = DifferenceImageObject(image_array[0], bg_image, crop_29, makeAnyColourDifferenceImage,
                                                 any_colour_reduce_noise, any_colour_noise_reduction_array)

if showFirstImageIndividually:
    fig, ax = plt.subplots()
    initial_difference_image.show_difference_image(ax)
    plt.show()
    initial_difference_image.show_colour_diff_img()

initialPolymerSample = PolymerSample(2, 0)
polymerModel = NCurveModel(curve_params, number_of_curves)
initial_polymer_sample = CurvedPolymerSample(initial_difference_image, initialPolymerSample,
                                             number_of_curves, polymerModel)
if testHSVNoiseReduction:
    rows, columns = 5, 5
    limits_array = [0, 100, 150, 255]
    choice = 2
    make_hsv_comparison_grid(initial_difference_image, rows, columns, limits_array, choice,
                             any_colour_noise_reduction_array)

if makingGrid or makingCurveComparison:
    sample_array = make_sample_array(image_array, currents_array, initial_polymer_sample)
    # for sample in sample_array:
    #    sample.difference_image_obj.show_colour_diff_img()

if makingGrid:
    make_sample_fit_grid(sample_array)

if makingCurveComparison:
    make_sample_curve_comparison(sample_array)
