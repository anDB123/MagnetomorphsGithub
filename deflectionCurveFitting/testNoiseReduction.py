import numpy as np

from imports import *


def plotNoiseReductionGrid(rows, columns, sample, lower_lower, lower_upper, upper_lower, upper_upper):
    # makes grid of plots and makes heatmap of chi-squareds
    print("Performing noise reduction test with {} rows and {} columns for a total of {} samples".format(rows, columns,
                                                                                                         rows * columns))
    noise_test_sample_array = []
    counter = 0
    lower_linspace, upper_linspace = np.linspace(lower_lower, lower_upper, rows), np.linspace(upper_lower, upper_upper,
                                                                                              columns)
    meshgrid_lower, meshgrid_upper = np.linspace(lower_lower, lower_upper, rows + 1), \
                                     np.linspace(upper_lower, upper_upper, columns + 1)
    total_start_time = time.time()
    for i in lower_linspace:
        for j in upper_linspace:
            start_time = time.time()
            print("i = {}, j = {}".format(i, j))
            temp_sample = copy.deepcopy(sample.changeNoiseReduction(i, j))
            noise_test_sample_array.append(temp_sample)
            counter += 1
            time_taken = time.time() - start_time
            print(
                "made noise reduction sample {} out of {} in {:.2f} seconds".format(counter, columns * rows,
                                                                                    time_taken))
    print("Time to make {} samples was {:.2f} seconds".format(rows * columns, time.time() - total_start_time))
    # ----------------make grid of plots------------------------------------
    fig, axs = plt.subplots(rows, columns)
    chi_squared_array = np.array([noise_test_sample.redChiSq for noise_test_sample in noise_test_sample_array])
    chi_squared_array = np.where(chi_squared_array > 0, chi_squared_array, np.nan)
    chi_squared_mesh = np.reshape(chi_squared_array, (rows, columns))
    print("Making plot of model")
    for sample, ax in zip(noise_test_sample_array, axs.flat): sample.makePlotOfModel(ax)
    plt.show()

    # ---------------make heatmap of chi-squareds----------------------------------

    x_mesh, y_mesh = np.meshgrid(meshgrid_lower, meshgrid_upper)
    fig, ax0 = plt.subplots()
    ax0.set_facecolor('black')
    ax0.set_xlabel("Lower Bound")
    ax0.set_ylabel("Upper Bound")
    cmap = plt.get_cmap('Purples')
    norm = mpl.colors.LogNorm(vmin=1, vmax=10)
    im = ax0.pcolormesh(x_mesh, y_mesh, chi_squared_mesh.transpose(), cmap=cmap, norm=norm)
    cbar = fig.colorbar(im, ax=ax0, ticks=[1, 1.5, 2, 2.5, 3, 3.5, 4, 4, 5, 5, 6, 7, 8, 9, 10])
    cbar.ax.set_yticklabels(['1', ' 1.5', ' 2', ' 2.5', ' 3', ' 3.5', '4', '4', '5', '5', '6', '7', '8', '9', '10'])
    cbar.set_label('Reduced Chi Squared', rotation=270, labelpad=30)
    plt.show()
