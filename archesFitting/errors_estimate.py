import copy

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
any_colour_noise_reduction_array = [[0, 255], [0, 255], [180, 250]]

thickness = 2 * 10 ** -3  # it was about 1 mm
width = 10 * 10 ** -3  # made to be exactly 1cm
youngModulus = 871931.69  # in pa found elsewhere in code (871931.69)
total_length = 20 * 10 ** -3  # around 6cm (this should not affect curve shape but will in this case)
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
physicalModel = PhysicalModelManyCurvesGradient(currents_array[0], properties_array, [0] * number_of_curves)

physicalModel.update_current(currents_array[0])
initial_polymer_sample = CurvedPolymerSample(initial_difference_image, initialPolymerSample,
                                             number_of_curves, physicalModel)
initial_curves = initial_polymer_sample.shapeFitModel.min_curvatures
"""
print(initial_curves)
fig, ax = plt.subplots(figsize=(10, 3))
# initial_polymer_sample.difference_image_obj.show_difference_image(ax)
initial_polymer_sample.plot_model(ax)
plt.axis('off')
plt.tight_layout()
plt.savefig("./comparison.pdf")
plt.show()
"""
difference_array = []
for i in range(0, 8):
    temp_properties_array = [thickness, width, youngModulus, total_length, magnet_thickness, magnet_mass,
                             magnet_strength, density]
    temp_properties_array[i] *= 1.01
    initial_difference_image = DifferenceImageObject(image_array[0], bg_image, crop_29, useOriginalImageForFilter,
                                                     any_colour_reduce_noise, any_colour_noise_reduction_array)
    initialPolymerSample = PolymerSample(thickness, currents_array[0])
    physicalModel = PhysicalModelManyCurvesGradient(currents_array[0], temp_properties_array, [0] * number_of_curves)

    physicalModel.update_current(currents_array[0])
    initial_polymer_sample = CurvedPolymerSample(initial_difference_image, initialPolymerSample,
                                                 number_of_curves, physicalModel)
    new_curves = initial_polymer_sample.shapeFitModel.min_curvatures
    initial_curves, new_curves = np.array(initial_curves), np.array(new_curves)
    difference = np.std((initial_curves - new_curves))
    print(f"Difference for {i} = {difference}")
    difference_array.append(difference)

temp_properties_array = [thickness, width, youngModulus, total_length, magnet_thickness, magnet_mass,
                         magnet_strength, density]
temp_current = currents_array[0] * 1.01
initial_difference_image = DifferenceImageObject(image_array[0], bg_image, crop_29, useOriginalImageForFilter,
                                                 any_colour_reduce_noise, any_colour_noise_reduction_array)
initialPolymerSample = PolymerSample(thickness, temp_current)
physicalModel = PhysicalModelManyCurvesGradient(temp_current, temp_properties_array, [0] * number_of_curves)

physicalModel.update_current(temp_current)
initial_polymer_sample = CurvedPolymerSample(initial_difference_image, initialPolymerSample,
                                             number_of_curves, physicalModel)
new_curves = initial_polymer_sample.shapeFitModel.min_curvatures
initial_curves, new_curves = np.array(initial_curves), np.array(new_curves)
difference = np.std((initial_curves - new_curves))
print(f"Difference for current = {difference}")
difference_array.append(difference)
plt.bar(["Thickness", "Width", "Young's Modulus", "Length", "Magnet Volume", "Magnet Mass",
         "Magnet Strength", "Density", "Current"], difference_array)
plt.xticks(rotation=45)
plt.ylabel("Relative Error")
plt.subplots_adjust(bottom=0.4)
plt.show()
plt.savefig("./errors_comparison.pdf")
