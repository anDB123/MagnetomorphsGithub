import matplotlib.pyplot as plt
import numpy as np

from imports import *

testNoiseReduction = False
testCropping = False
makingGrid = True
makingCurveComparison = False
showFirstImageIndividually = False
testHSVNoiseReduction = False

graph_dir = "C:/Users/AndyPC/Desktop/MagnetomorphsGithub/graphs"

folder_name = "matt_black_background_test3"
image_array = ["../{}/DS_00{}.JPG".format(folder_name, i) for i in
               ["01", "02", "03", "04", "05"]]  # goes to 68
bg_image = "../matt_black_background_test4/DS_0006.JPG"

currents_array = np.linspace(0, 4, 5)

crop_29 = [600, 1300, 300, 2800]
any_colour_noise_reduction_array = [[0, 255], [0, 255], [200, 255]]

thickness = 2 * 10 ** -3  # it was about 1 mm
width = 10 * 10 ** -3  # made to be exactly 1cm
youngModulus = 871931.69  # in pa found elsewhere in code
total_length = 55 * 10 ** -3  # around 6cm (this should not affect curve shape but will in this case)
magnet_thickness = 4 * 10 ** -3  # 4mm thick magnet
magnet_mass = 0.3566 * 10 ** -3  # 0.3566g magnet
magnet_strength = 1.2  # measured in tesla
field_strength = 6 * 10 ** - 3  # 6 mT as measured with gaussmeter
density = 1161  # assumed same as water
number_of_curves = 30

properties_array = [thickness, width, youngModulus, total_length, magnet_thickness, magnet_mass, magnet_strength,
                    field_strength, density]
init_vals = [10000, 0, 0]
circle_bounds = [[1, 0, 0], [np.inf, np.inf, np.inf]]
curve_params = [circle_fit, init_vals, circle_bounds]

initial_difference_image = DifferenceImageObject(image_array[0], bg_image, crop_29, useOriginalImageForFilter,
                                                 any_colour_reduce_noise, any_colour_noise_reduction_array)
initialPolymerSample = PolymerSample(0, 0)

physicalModel = PhysicalModelManyCurvesOptimised(currents_array[0], properties_array, [0] * 10)
physicalModel.update_current(0)
if showFirstImageIndividually:
    fig, ax = plt.subplots()
    initial_difference_image.show_difference_image(ax)
    plt.show()
    initial_difference_image.show_colour_diff_img()

initial_polymer_sample = CurvedPolymerSample(initial_difference_image, initialPolymerSample,
                                             number_of_curves, physicalModel)
if testHSVNoiseReduction:
    make_hsv_comparison_grid(initial_difference_image, 5, 5, [0, 100, 150, 255], 2,
                             any_colour_noise_reduction_array)

if makingGrid or makingCurveComparison:
    sample_array = make_sample_array(image_array, currents_array, initial_polymer_sample)

if makingGrid: make_sample_fit_grid(sample_array)

if makingCurveComparison: make_sample_curve_comparison(sample_array)
