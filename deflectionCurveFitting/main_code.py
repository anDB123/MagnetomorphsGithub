from imports import *

testNoiseReduction = False
testCropping = False
makingGrid = True
makingCurveComparison = False

graph_dir = "C:/Users/AndyPC/Desktop/MagnetomorphsGithub/graphs"
image_array = ["../29redBackground/DSC_00{} (3).JPG".format(i) for i in range(59, 68)]
bg_image = "../29redBackground/DSC_0068 (3).JPG"
currents_array = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]

crop_29 = [130, 1200, 300, 2800]
noise_reduction = [100, 210]
curve_start, curve_end, curve_params = 1600, 2000, [10000, 1800, 800]

initial_polymer_sample = curvedPolmerSample(image_array[0], bg_image, crop_29, 2, currents_array[0],
                                            noise_reduction, curve_start, curve_end, curve_params)

if testNoiseReduction:
    plotNoiseReductionGrid(10, 10, initial_polymer_sample, 60, 160, 170, 240)

if makingGrid or makingCurveComparison:
    sample_array = make_sample_array(image_array, bg_image, crop_29, currents_array, noise_reduction,
                                     initial_polymer_sample)

if makingGrid:
    make_sample_fit_grid(sample_array)

if makingCurveComparison:
    make_sample_curve_comparison(sample_array)
