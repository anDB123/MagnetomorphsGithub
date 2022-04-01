import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

top_init_vals = [1, 1]

def two_lines(x, a, b, c, d, e):
    if x <= a:
        return b * x + c
    return d * x + e

def one_line(x, a, b):
    return a * x + b

def get_gradient(filename):
    top_data = np.genfromtxt(filename, skip_header=1, delimiter=',')
    extension_vals = top_data[:, 0]
    force_vals = top_data[:, 1]
    best_vals, covarA = curve_fit(one_line, extension_vals, force_vals, p0=top_init_vals)
    return best_vals[0]

def find_min_residual(extension_vals, force_vals):
    cutPoints = []
    sum_residual_square = []
    for cutPoint in range(5, len(extension_vals) - 5):
        extension_valsA = extension_vals[:cutPoint]
        extension_valsB = extension_vals[cutPoint:]
        force_valsA = force_vals[:cutPoint]
        force_valsB = force_vals[cutPoint:]


        best_top_valsA, covarA = curve_fit(one_line, extension_valsA, force_valsA, p0=top_init_vals)
        best_top_valsB, covarB = curve_fit(one_line, extension_valsB, force_valsB, p0=top_init_vals)
        fitted_lines = np.append(one_line(extension_valsA, *best_top_valsA), one_line(extension_valsB, *best_top_valsB))
        residuals = fitted_lines - force_vals
        cutPoints.append(cutPoint)
        sum_residual_square.append(np.sum(residuals ** 2))
        print(np.sum(residuals ** 2))

    min_residual = np.min(sum_residual_square)

    cutPoint = cutPoints[np.where(min_residual == sum_residual_square)[0][0]]
    return cutPoint


# top measurement

def get_top_or_bottom(filename,pos,plottitle):
    top_data = np.genfromtxt(filename, skip_header=1, delimiter=',')
    extension_vals = top_data[:, 0]
    force_vals = top_data[:, 1]

    cutPoint = find_min_residual(extension_vals, force_vals)
    extension_valsA = extension_vals[:cutPoint]
    extension_valsB = extension_vals[cutPoint:]
    force_valsA = force_vals[:cutPoint]
    force_valsB = force_vals[cutPoint:]
    best_top_valsA, covarA = curve_fit(one_line, extension_valsA, force_valsA, p0=top_init_vals)
    best_top_valsB, covarB = curve_fit(one_line, extension_valsB, force_valsB, p0=top_init_vals)

    plt.subplot(pos)
    plt.scatter(extension_vals,force_vals)
    plt.plot(extension_valsA, one_line(extension_valsA, *best_top_valsA), c='red')
    plt.plot(extension_valsB, one_line(extension_valsB, *best_top_valsB), c='red')
    plt.xlabel("Extension (mm)")
    plt.ylabel("Force (N)")
    plt.title(plottitle)
    return extension_vals[cutPoint]

top_file = "youngsModulusMeasurements/polymer_top.csv"
bot_file = "youngsModulusMeasurements/polymer_bottom.csv"
diam_top_file = "youngsModulusMeasurements/diameter_top.csv"
diam_bot_file = "youngsModulusMeasurements/diameter_bottom.csv"
top_of_polymer = get_top_or_bottom(top_file,221,"Top of Polymer")
bot_of_polymer = get_top_or_bottom(bot_file,222,"Bottom of Polymer")
top_of_diam = get_top_or_bottom(diam_top_file,223,"Top of Diameter")
bot_of_diam = get_top_or_bottom(diam_bot_file,224,"Bottom of Diameter")
plt.show()
print("Top of polymer at %f mm"%top_of_polymer)
print("Bottom of polymer at %f mm"%bot_of_polymer)
thickness = bot_of_polymer-top_of_polymer

# diam top


diameter = bot_of_diam-top_of_diam
print("Top of diameter at %f mm"%top_of_diam)
print("Bottom of diameter at %f mm"%bot_of_diam)

# diam bot
# force extenstion
force_ext_file = "youngsModulusMeasurements/force_extension.csv"
force_extension_gradient = get_gradient(force_ext_file)


# youngs modulus calc
area = 1/4*diameter**2
YoungModulus = force_extension_gradient/area*thickness
print("Thickness of polymer of %f mm"%(thickness))
print("Diameter of %f mm"%(diameter))
print("Gradient of %f N/mm"%(force_extension_gradient))
print("Young's Modulus of %f Pa"%(YoungModulus*10**6))
print("Young's Modulus of %f MPa"%(YoungModulus))
