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

folder_name = "\matt_black_arch_test"
image_array = ["../{}/asample{}.JPG".format(folder_name, i) for i in range(5, 6)]  # goes to 68
bg_image = "../matt_black_10_samples125/asample6.JPG"
# currents_array = [0, 0.498, 1.021, 1.509, 1.971, 2.522, 3.060, 3.586, 3.975]
currents_array = [-3.975]

crop_29 = [800, 1300, 800, 2900]
any_colour_noise_reduction_array = [[0, 255], [0, 255], [200, 250]]

thickness = 1.2 * 10 ** -3  # it was about 1 mm
width = 10 * 10 ** -3  # made to be exactly 1cm
youngModulus = 871931.69  # in pa found elsewhere in code (871931.69)
total_length = 60 * 10 ** -3  # around 6cm (this should not affect curve shape but will in this case)
magnet_thickness = 4 * 10 ** -3  # 4mm thick magnet
magnet_mass = 0.3566 * 10 ** -3  # 0.3566g magnet
magnet_strength = 1.2  # measured in tesla (from website)
field_strength = 6 * 10 ** - 3  # 6 mT as measured with gaussmeter
density = 1161  # measured from puck (1161)
number_of_curves = 10

properties_array = [thickness, width, youngModulus, total_length, magnet_thickness, magnet_mass, magnet_strength,
                    field_strength, density]

initial_difference_image = DifferenceImageObject(image_array[0], bg_image, crop_29, useOriginalImageForFilter,
                                                 any_colour_reduce_noise, any_colour_noise_reduction_array)
initialPolymerSample = PolymerSample(thickness, currents_array[0])

physicalModel = PhysicalModelManyCurvesGradient(currents_array[0], properties_array, [0] * number_of_curves)
physicalModel.update_current(currents_array[0])
initial_polymer_sample = CurvedPolymerSample(initial_difference_image, initialPolymerSample,
                                             number_of_curves, physicalModel)
if showFirstImageIndividually:
    fig, ax = plt.subplots()

    initial_difference_image.show_difference_image(ax)
    # initial_polymer_sample.plot_errorbars(ax)
    plt.scatter(initial_polymer_sample.x_data, initial_polymer_sample.y_data, s=10)
    plt.show()

    # initial_difference_image.show_colour_diff_img()
    # plt.show()
    # initial_polymer_sample.plot_model(ax)
    # ax.invert_yaxis()

if testHSVNoiseReduction:
    make_hsv_comparison_grid(initial_difference_image, 5, 5, [0, 100, 150, 255], 2,
                             any_colour_noise_reduction_array)

if makingGrid or makingCurveComparison:
    sample_array = make_sample_array(image_array, currents_array, initial_polymer_sample)

if makingGrid: make_sample_fit_grid(sample_array)

if makingCurveComparison: make_sample_curve_comparison(sample_array)
