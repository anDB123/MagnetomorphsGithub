import copy

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

def get_top_or_bottom(filename, pos, plottitle):
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

    # plt.subplot(pos)
    # plt.scatter(extension_vals, force_vals)
    # plt.plot(extension_valsA, one_line(extension_valsA, *best_top_valsA), c='red')
    # plt.plot(extension_valsB, one_line(extension_valsB, *best_top_valsB), c='red')
    # plt.xlabel("Extension (mm)")
    # plt.ylabel("Force (N)")
    # plt.title(plottitle)
    return extension_vals[cutPoint]


top_file = "youngsModulusMeasurements/polymer_top.csv"
bot_file = "youngsModulusMeasurements/polymer_bottom.csv"
diam_top_file = "youngsModulusMeasurements/diameter_top.csv"
diam_bot_file = "youngsModulusMeasurements/diameter_bottom.csv"
top_of_polymer = get_top_or_bottom(top_file, 221, "Top of Polymer")
bot_of_polymer = get_top_or_bottom(bot_file, 222, "Bottom of Polymer")
top_of_diam = get_top_or_bottom(diam_top_file, 223, "Top of Diameter")
bot_of_diam = get_top_or_bottom(diam_bot_file, 224, "Bottom of Diameter")
# plt.show()
print("Top of polymer at %f mm" % top_of_polymer)
print("Bottom of polymer at %f mm" % bot_of_polymer)
thickness = bot_of_polymer - top_of_polymer

# diam top


diameter = bot_of_diam - top_of_diam
# print("Top of diameter at %f mm"%top_of_diam)
# print("Bottom of diameter at %f mm"%bot_of_diam)

# diam bot
# force extenstion
force_ext_file = "youngsModulusMeasurements/force_extension.csv"
force_extension_gradient = get_gradient(force_ext_file)


# youngs modulus calc

def chi_squared(y_data, y_errors, y_model):
    chi_squared = 0
    for y_value, y_error, y_model_value in zip(y_data, y_errors, y_model):
        chi_squared += (y_value - y_model_value) ** 2 / y_error ** 2
    return chi_squared


def find_gradient_and_chi_squared_and_error(x_data, y_data, errors):
    y_data = np.array(y_data)
    x_data = np.array(x_data)
    gradient = (y_data[-1] - y_data[0]) / (x_data[-1] - x_data[0])  # initial_guess
    continue_bool = True
    resolution = 1
    while continue_bool:
        current_model_data = (x_data - x_data[0]) * gradient + y_data[0]
        current_chi_squared = chi_squared(y_data, errors, current_model_data)
        upper_gradient = gradient + resolution
        lower_gradient = gradient - resolution
        upper_model_data = (x_data - x_data[0]) * upper_gradient + y_data[0]
        upper_chi_squared = chi_squared(y_data, errors, upper_model_data)
        lower_model_data = (x_data - x_data[0]) * lower_gradient + y_data[0]
        lower_chi_squared = chi_squared(y_data, errors, lower_model_data)
        if lower_chi_squared < current_chi_squared:
            gradient = lower_gradient
        elif upper_chi_squared < current_chi_squared:
            gradient = upper_gradient
        elif resolution > 10 ** -6:
            resolution *= 0.1
            print("Reducing resolution")
        else:
            continue_bool = False
    best_gradient_error = 0
    for gradient_error in np.linspace(0, gradient, 100000):
        test_gradient = gradient + gradient_error
        test_model_data = (x_data - x_data[0]) * test_gradient + y_data[0]
        test_chi_squared = chi_squared(y_data, errors, test_model_data)
        if test_chi_squared > (current_chi_squared + 1):
            best_gradient_error = gradient_error
            break

    return current_chi_squared, gradient, gradient_error


def find_errors(y_data):
    y_data = np.array(y_data)
    error_range = 10
    errors_array = y_data
    for i in range(error_range, len(y_data) - error_range):
        assessed_data = copy.deepcopy(y_data[i - error_range:i + error_range])
        gradient = (assessed_data[-1] - assessed_data[0]) / (2 * error_range + 1)
        pre_adjusted_error = np.std(assessed_data)
        for j in range(len(assessed_data)):
            assessed_data[j] = assessed_data[j] - gradient * j
        errors_array[i] = np.std(assessed_data, ddof=1) / np.sqrt(np.size(assessed_data))
        print(f"gradient={gradient}, pre_adjusted = {pre_adjusted_error},error = {errors_array[i]}")

    errors_array[0:error_range] = np.mean(errors_array[error_range:3 * error_range])
    errors_array[-error_range:-1] = np.mean(errors_array[- 3 * error_range:- error_range])
    errors_array[-1] = errors_array[-2]
    return errors_array


def makeYoungModulusGraph(ax):
    top_data = np.genfromtxt(force_ext_file, skip_header=1, delimiter=',')
    first_val = 200
    last_val = 1
    extension_vals = top_data[:, 0]
    force_vals = top_data[:, 1]
    errors_array = find_errors(force_vals)
    ax.errorbar(extension_vals, force_vals, yerr=errors_array, fmt='')
    chi_squared, graph_gradient, graph_gradient_error = find_gradient_and_chi_squared_and_error(
        extension_vals[-first_val:],
        force_vals[-first_val:],
        errors_array[-first_val:])
    print(f"chi_squared = {chi_squared}, graph_gradient = {graph_gradient}")
    ax.plot(extension_vals[-first_val:-last_val],
            (np.array(extension_vals[-first_val:-last_val]) - extension_vals[-first_val]) * graph_gradient +
            force_vals[-first_val], c='k')
    ax.set_xlabel("Extension ($\mu m$)")
    ax.set_ylabel("Force (N)")
    area = 1 / 4 * diameter ** 2
    real_gradient = graph_gradient * 10 ** 6
    real_error = graph_gradient_error * 10 ** 6
    YoungModulus = real_gradient / area * thickness
    YoungModulusError = real_error / area * thickness
    ax.text(0.5, 25, f"Young's Modulus = {YoungModulus} $\pm$ {YoungModulusError} Pa", color='k', fontsize=13)
    print(
        f"Young's Modulus = {YoungModulus} $\pm$ {YoungModulusError} Pa % err = {YoungModulusError / YoungModulus * 100}%")
    print("Young's Modulus of %f Pa" % (YoungModulus * 10 ** 6))

# print("Thickness of polymer of %f mm"%(thickness))
# print("Diameter of %f mm"%(diameter))
# print("Gradient of %f N/mm"%(force_extension_gradient))
# print("Young's Modulus of %f Pa"%(YoungModulus*10**6))
# print("Young's Modulus of %f MPa"%(YoungModulus))
