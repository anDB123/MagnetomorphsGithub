import matplotlib.pyplot as plt
import numpy as np

from imports import *

testNoiseReduction = False
testCropping = False
makingGrid = False
makingCurveComparison = False
showFirstImageIndividually = False
testHSVNoiseReduction = True

graph_dir = "C:/Users/AndyPC/Desktop/MagnetomorphsGithub/graphs"
image_array = ["../29redBackground/DSC_00{} (3).JPG".format(i) for i in range(59, 68)]
bg_image = "../29redBackground/DSC_0068 (3).JPG"
currents_array = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]

crop_29 = [130, 1200, 300, 2800]
blue_only_noise_reduction = [100, 210]

lowH, highH = 100, 180
lowS, highS = 0, 200
lowV, highV = 10, 250

any_colour_noise_reduction_array = [lowH, highH, lowS, highS, lowV, highV]
thickness = 2
number_of_curves = 30

initial_polymer_sample = curvedPolmerSample(image_array[0], bg_image, crop_29, thickness, currents_array[0],
                                            makeAnyColourDifferenceImage,
                                            any_colour_reduce_noise, any_colour_noise_reduction_array, number_of_curves)
if showFirstImageIndividually:
    fig, ax = plt.subplots()
    initial_polymer_sample.plotImageWithEdgesAndModel(ax)
    plt.show()

if testNoiseReduction:
    plotNoiseReductionGrid(10, 10, initial_polymer_sample, 60, 160, 170, 240)

if testHSVNoiseReduction:
    rows, columns = 3, 3
    fig, axs = plt.subplots(rows, columns)
    hue_min_vals = np.linspace(10, 100, rows)
    hue_max_vals = np.linspace(120, 170, columns)
    for i in range(rows):
        for j in range(columns):
            hsv_limits = hue_min_vals[i], hue_max_vals[j], 0, 255, 0, 255
            initial_polymer_sample.changeHSVNoiseReduction(hsv_limits)
            initial_polymer_sample.plotDifferenceImage(axs[i, j])
    plt.show()
if makingGrid or makingCurveComparison:
    sample_array = make_sample_array(image_array, currents_array, initial_polymer_sample)

if makingGrid:
    make_sample_fit_grid(sample_array)

if makingCurveComparison:
    make_sample_curve_comparison(sample_array)
