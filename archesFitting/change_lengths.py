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


crop_29 = [800, 1300, 800, 2900]
any_colour_noise_reduction_array = [[0, 255], [0, 255], [180, 250]]

thickness = 2 * 10 ** -3  # it was about 1 mm 5
width = 4 * 10 ** -3  # made to be exactly 1cm
youngModulus = 871931.69  # in pa found elsewhere in code (871931.69)
total_length = 45 * 10 ** -3  # around 6cm (this should not affect curve shape but will in this case)
magnet_thickness = 4 * 10 ** -3  # 4mm thick magnet
magnet_mass = 0.3566 * 10 ** -3  # 0.3566g magnet
magnet_strength = 1.2  # measured in tesla (from website)
density = 1161  # measured from puck (1161)
number_of_curves = 100

"""
fig, ax = plt.subplots()
initial_difference_image.show_difference_image(ax)
plt.show()
"""

"""
fig, ax = plt.subplots(figsize=(5, 5))
# initial_polymer_sample.difference_image_obj.show_difference_image(ax)
# initial_polymer_sample.plotImageWithEdgesAndModel(ax)
plt.axis('off')
plt.tight_layout()
plt.savefig("./arch_fit.pdf")
plt.show()
"""

properties_array = [thickness, width, youngModulus, total_length, magnet_thickness, magnet_mass, magnet_strength,
                    density]

initial_difference_image = DifferenceImageObject(image_array[0], bg_image, crop_29, useOriginalImageForFilter,
                                                 any_colour_reduce_noise, any_colour_noise_reduction_array)

currents_array = np.linspace(-15, 0, 10)
lengths_array = np.linspace(10 * 10 ** -3, 100 * 10 ** -3, 100)
heights_array = []
x_data_array = []
y_data_array = []
initialPolymerSample = PolymerSample(thickness, currents_array[0])
"""
physicalModel = PhysicalModelManyCurvesGradient(currents_array[0], properties_array, [0] * number_of_curves)
"""
for length in lengths_array:
    print("Making polymer sample")
    properties_array = [thickness, width, youngModulus, length, magnet_thickness, magnet_mass, magnet_strength,
                        density]

    physicalModel = PhysicalModelManyCurvesGradient(-4, properties_array, [0] * number_of_curves)
    physicalModel.update_current(-4)
    initial_polymer_sample = CurvedPolymerSample(initial_difference_image, initialPolymerSample,
                                                 number_of_curves, physicalModel)
    x_data = initial_polymer_sample.shapeFitModel.model_x_data
    y_data = initial_polymer_sample.shapeFitModel.model_y_data

    height = np.abs(y_data[0] - y_data[-1]) / (initial_polymer_sample.shapeFitModel.scaling / 1000)
    print(f"Height = {height}")
    heights_array.append(height)
    x_data = x_data - x_data[0]
    y_data = np.max(y_data) - y_data
    x_data *= 1 / (initial_polymer_sample.shapeFitModel.scaling / 1000)
    y_data *= 1 / (initial_polymer_sample.shapeFitModel.scaling / 1000)
    x_data_array.append(x_data)
    y_data_array.append(y_data)
    print(x_data)
    print(x_data_array)

fig, axd = plt.subplot_mosaic([['left', 'right1'],
                               ['left', 'right2'],
                               ['left', 'right3'],
                               ['left', 'right4']],
                              constrained_layout=True)
lengths_array = np.array(lengths_array)
lengths_array *= 10 ** 3
currents_array = np.array(currents_array)
currents_array *= -1.5

axd['left'].plot(lengths_array, heights_array)
axd['left'].set_ylabel("Height of Centre (mm)")
axd['left'].set_xlabel("Leg length (mm)")

colors = ['r', 'g', 'b', 'y']
ind_pos = [10, 30, 50, 70]
currents_array = np.array(currents_array)
lengths_array = np.array(lengths_array)
heights_array = np.array(heights_array)
axd['left'].scatter(lengths_array[ind_pos], heights_array[ind_pos], color=colors)

for ax, i, j in zip([axd['right1'], axd['right2'], axd['right3'], axd['right4']], (0, 1, 2, 3), ind_pos):
    x_data = np.array(x_data_array[j])
    y_data = np.array(y_data_array[j])
    x_data = np.append(-x_data[::-1], x_data)
    y_data = np.append(y_data[::-1], y_data)
    ax.plot(x_data, y_data, f'{colors[i]}-')
    ax.set_xlim(-80, 80)
    ax.set_ylim(-2, 16)
    ax.set_aspect('equal')
axd['right4'].set_xlabel("X Values (mm)")
axd['right4'].set_ylabel("Y Values (mm)")
plt.show()
print("Finished plots")
