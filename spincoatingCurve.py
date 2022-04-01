import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from modelFunctions import *
from fitting_code import *

measurements_folder = "Confocal Laser Measurements"
rpm_array = [50, 100, 200, 400]
sample_array = [
    "50 sample.csv",
    "100 sample.csv",
    "200 sample.csv",
    "400 sample.csv",
]
background_array = [
    "50 no sample.csv",
    "100 no sample.csv",
    "200 no sample.csv",
    "400 no sample.csv",
]

scale_factor_array = [1 / 10000, 1 / 10000, 1 / 100000, 1 / 100000]
bg_scale_factor_array = [1 / 10000, 1 / 10000, 1 / 10000, 1 / 10000]
thickness_array = []
thickness_error_array = []
for i in range(len(sample_array)):
    file_name = measurements_folder + '/' + sample_array[i]
    background_file_name = measurements_folder + '/' + background_array[i]
    sample_data = np.genfromtxt(file_name)
    sample_data = sample_data * scale_factor_array[i]
    sample_mean = np.mean(sample_data)
    sample_error = np.std(sample_data, ddof=1)
    background_data = np.genfromtxt(background_file_name)
    background_data = background_data * bg_scale_factor_array[i]
    background_mean = np.mean(background_data)
    print(sample_mean)
    print(background_mean)
    background_error = np.std(background_data, ddof=1)
    thickness = abs(background_mean - sample_mean)
    thickness_array.append(thickness)
    thickness_error_array.append(np.sqrt(background_error + sample_error))

# plt.scatter(rpm_array,thickness_array)
plt.errorbar(rpm_array, thickness_array, ecolor='k', yerr=thickness_error_array, linestyle='',
             label="Confocal Laser Data")  # ,)

thickness_array = np.array(thickness_array)
thickness_error_array = np.array(thickness_error_array)

plt.ylabel("Thickness ($mm$)")
plt.xlabel("RPM")

fitted_params, fit_matrix = curve_fit(exponential_curve, rpm_array, thickness_array, p0=exp_init_vals)
x_fit_vals = np.linspace(np.min(rpm_array), np.max(rpm_array), 1000)
y_fit_vals = exponential_curve(x_fit_vals, *fitted_params)
y_test = []
for i in rpm_array:
    y_test = np.append(y_test, exponential_curve(i, *fitted_params))
red_chi_squared = find_reduced_chi_squared(thickness_array, y_test, thickness_error_array)

plt.plot(x_fit_vals, y_fit_vals, label="Exponential Fit $\chi _r^2$ = {:.2f}".format(red_chi_squared))

plt.legend()
plt.show()
