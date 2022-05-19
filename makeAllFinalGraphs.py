import matplotlib.pyplot as plt
import region_of_uniformity
import youngsModulusAnalysis

from imports import *

# universal options
plt.rcParams['font.size'] = 10

# plt.rcParams['text.usetex'] = True
fig_size = (10, 6)
output_file = "./reportPhotos"
# make region of uniformity plot
"""
fig, ax = plt.subplots(figsize=fig_size)
fig.tight_layout()
region_of_uniformity.makeRegionOfUniformityPlot(ax)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(bottom=0.2)
plt.savefig(f"{output_file}/magnetic_uniform_region.pdf")
# plt.show()
plt.close(fig)
# make young's modulus graph
fig, ax = plt.subplots(figsize=fig_size)
fig.tight_layout()
youngsModulusAnalysis.makeYoungModulusGraph(ax)
plt.savefig(f"{output_file}/youngModulusAnalysis.pdf")
# plt.show()
plt.close(fig)
#

# rpm-thickness curve
import spincoatingCurve

fig, ax = plt.subplots(figsize=fig_size)
fig.tight_layout()
spincoatingCurve.makeSpincoatCurve(ax)
plt.subplots_adjust(left=0.15)
plt.savefig(f"{output_file}/spincoatingCurve.pdf")

plt.show()
plt.close(fig)
"""
# background removal example

folder_name = "matt_black_background_testFINAL"
image_array = [f"{folder_name}/asample{i}.JPG" for i in range(1, 9)]  # goes to 68
bg_image = "matt_black_10_samples125/asample8.JPG"
currents_array = [3.975]
crop_29 = [600, 1300, 600, 2000]
any_colour_noise_reduction_array = [[0, 255], [0, 255], [170, 250]]

initial_difference_image = DifferenceImageObject(image_array[0], bg_image, crop_29, useOriginalImageForFilter,
                                                 any_colour_reduce_noise, any_colour_noise_reduction_array)

"""
fig, axs = plt.subplots(2, 1, figsize=fig_size)
axs[0].set_title("Original Image")
img = cv.imread("matt_black_10_samples125/asample9.JPG", cv.IMREAD_COLOR)[crop_29[0]:crop_29[1], crop_29[2]:crop_29[3]]
axs[0].imshow(img[:, :, 2])
"""
difference_image = initial_difference_image.difference_image
"""
axs[1].imshow(difference_image)
axs[1].set_title("Background Removed")
plt.subplots_adjust(hspace=0.5)
plt.savefig(f"{output_file}/background_removal_example.pdf")
plt.show()
"""
"""
fig, axs = plt.subplots(figsize=fig_size)
difference_image = initial_difference_image.difference_image
axs.imshow(difference_image)
x_means, y_means, y_errors = makeCurveFromDifferenceImage(difference_image, 100, 200, 3)
axs.scatter(x_means, y_means, s=1, label="Detected bottom edge")
axs.legend()
plt.savefig(f"{output_file}/edge_detection_example.pdf")
plt.show()
"""

# showing physical model shape
thickness = 2 * 10 ** -3  # it was about 1 mm
width = 10 * 10 ** -3  # made to be exactly 1cm
youngModulus = 871931.69  # in pa found elsewhere in code
total_length = 65 * 10 ** -3  # around 6cm (this should not affect curve shape but will in this case)
magnet_thickness = 4 * 10 ** -3  # 4mm thick magnet
magnet_mass = 0.3566 * 10 ** -3  # 0.3566g magnet
magnet_strength = 0.4  # measured in tesla (from website)
field_strength = 6 * 10 ** - 3  # 6 mT as measured with gaussmeter
density = 1  # measured from puck (1161)
number_of_curves = 30
fig, ax = plt.subplots()
number_of_curves_array = [1, 2, 5, 10, 30, 50, 100]
for number_of_curves in number_of_curves_array:
    properties_array = [thickness, width, youngModulus, total_length, magnet_thickness, magnet_mass, magnet_strength,
                        density]
    currents_array = [4]
    physicalModel = PhysicalModelManyCurvesOptimised(currents_array[0], properties_array, [0] * number_of_curves)
    initialPolymerSample = PolymerSample(thickness, currents_array[0])
    initial_polymer_sample = CurvedPolymerSample(initial_difference_image, initialPolymerSample,
                                                 number_of_curves, physicalModel)
    x_data = initial_polymer_sample.shapeFitModel.model_x_data
    y_data = initial_polymer_sample.shapeFitModel.model_y_data
    x_data = (x_data - x_data[0]) * 60 / 1200
    y_data = (y_data[0] - y_data) * 60 / 1200
    ax.plot(x_data, y_data, label=f"{number_of_curves} Arcs")
ax.set_xlabel("Predicted X values (mm)")
ax.set_ylabel("Predicted Y values (mm)")
ax.set_aspect('equal')
ax.legend()
plt.savefig(f"{output_file}/curve_vs_number_of_arcs.pdf")
plt.show()
# printing chi squared values
