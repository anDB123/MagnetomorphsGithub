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

folder_name = "matt_black_background_testFINAL"
image_array = ["../{}/asample{}.JPG".format(folder_name, i) for i in range(0, 9)]  # goes to 68
bg_image = "../matt_black_10_samples125/asample7.JPG"
currents_array = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]

crop_29 = [600, 1300, 300, 2800]
any_colour_noise_reduction_array = [[0, 255], [0, 255], [180, 255]]

thickness = 1.2 * 10 ** -3  # it was about 1 mm
width = 10 * 10 ** -3  # made to be exactly 1cm
youngModulus = 1347819  # in pa found elsewhere in code
total_length = 55 * 10 ** -3  # around 6cm (this should not affect curve shape but will in this case)
magnet_thickness = 4 * 10 ** -3  # 4mm thick magnet
magnet_mass = 0.3566 * 10 ** -3  # 0.3566g magnet
magnet_strength = 1.2  # measured in tesla (from website)
field_strength = 6 * 10 ** - 3  # 6 mT as measured with gaussmeter
density = 1161  # measured from puck (1161)
number_of_curves = 30

properties_array = [thickness, width, youngModulus, total_length, magnet_thickness, magnet_mass, magnet_strength,
                    density]

initial_difference_image = DifferenceImageObject(image_array[0], bg_image, crop_29, useOriginalImageForFilter,
                                                 any_colour_reduce_noise, any_colour_noise_reduction_array)
initialPolymerSample = PolymerSample(thickness, currents_array[0])

physicalModel = PhysicalModelManyCurvesOptimised(currents_array[0], properties_array, [0] * number_of_curves)
physicalModel.update_current(currents_array[0])
initial_polymer_sample = CurvedPolymerSample(initial_difference_image, initialPolymerSample,
                                             number_of_curves, physicalModel)
if showFirstImageIndividually:
    fig, ax = plt.subplots()
    initial_polymer_sample.plot_model(ax)
    ax.invert_yaxis()
    plt.show()
if testHSVNoiseReduction:
    make_hsv_comparison_grid(initial_difference_image, 5, 5, [0, 100, 150, 255], 2,
                             any_colour_noise_reduction_array)

if makingGrid or makingCurveComparison:
    sample_array = make_sample_array(image_array, currents_array, initial_polymer_sample)

if makingGrid:
    fig1, ax = plt.subplots()
    # fig2, ax2 = plt.subplots()
    # ax.invert_yaxis()
    for sample in sample_array:
        x_data = sample.x_data - sample.x_data[0]
        y_data = -(sample.y_data - sample.y_data[0])
        model_x_data = sample.shapeFitModel.model_x_data - sample.shapeFitModel.model_x_data[0]
        model_y_data = -(sample.shapeFitModel.model_y_data - sample.shapeFitModel.model_y_data[0])
        x_data *= 9 / 2000
        y_data *= 9 / 2000
        model_x_data *= 9 / 2000
        model_y_data *= 9 / 2000
        new_x_data, new_y_data = [], []
        for i in range(len(x_data)):
            if i % 10 == 0:
                new_x_data.append(x_data[i])
                new_y_data.append(y_data[i])
        ax.scatter(new_x_data, new_y_data, s=10)
        ax.plot(model_x_data, model_y_data)
        ax.set_xlabel("X Values (cm)")
        ax.set_ylabel("Y Values (cm)")
        # sample.plotImageWithEdgesAndModel(ax)
plt.show()
# fig2.show()
