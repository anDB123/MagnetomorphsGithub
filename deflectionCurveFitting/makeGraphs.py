from imports import *


def make_sample_fit_grid(sample_array):
    fig, axs = plt.subplots(*(lambda c, t: (c, math.ceil(t / c)))(3, len(sample_array)))
    for sample, ax in zip(sample_array, axs.flat): sample.plotImageWithEdgesAndModel(ax)
    fig.canvas.manager.set_window_title('Test')
    plt.show()


def make_sample_curve_comparison(sample_array):
    fig, ax = plt.subplots()
    for sample in sample_array:
        sample.plot_errorbars(ax)
        sample.plot_model(ax)
    ax.invert_yaxis()
    plt.legend()
    plt.show()
