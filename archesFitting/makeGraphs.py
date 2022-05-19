from imports import *


def make_sample_curve_comparison(sample_array):
    fig, ax = plt.subplots()
    for sample in sample_array:
        sample.plot_errorbars(ax)
        sample.plot_model(ax)
    ax.invert_yaxis()
    plt.legend()
    plt.show()
