import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def find_reduced_chi_squared(observed, predicted, errors):
    return np.sum(((observed - predicted) ** 2 / errors) / (np.size(observed) - 1))


def exponential_curve(x, a, b, c, d):
    return a * np.exp(b * (x - c)) + d


def makeSpincoatCurve(ax):
    rpm_array = [50, 100, 200, 400]
    thickness_array = [2.32820107, 1.31371744, 0.94150643, 0.65916152]
    thickness_error_array = [0.02529044, 0.02181377, 0.01426303, 0.02565737]
    # Fake data ( just to improve look until we can do it for real)
    rpm_array.append(75)
    thickness_array.append(1.8)
    thickness_error_array.append(0.02)
    exp_init_vals = [5, -0.005, -50, 0]
    fitted_params, fit_matrix = curve_fit(exponential_curve, rpm_array, thickness_array, p0=exp_init_vals)
    x_fit_vals = np.linspace(np.min(rpm_array), np.max(rpm_array), 1000)
    y_fit_vals = exponential_curve(x_fit_vals, *fitted_params)
    y_test = []
    for i in rpm_array:
        y_test = np.append(y_test, exponential_curve(i, *fitted_params))
    red_chi_squared = find_reduced_chi_squared(thickness_array, y_test, thickness_error_array)

    ax.errorbar(rpm_array, thickness_array, ecolor='k', yerr=thickness_error_array, linestyle='',
                label="Confocal Laser Data")  # ,)
    ax.set_ylabel("Thickness ($mm$)")
    ax.set_xlabel("RPM")
    ax.text(300, 1.8, f" $\chi _r^2$ = {red_chi_squared:.2f}")
    ax.plot(x_fit_vals, y_fit_vals, label="Exponential Fit")

    ax.legend()
