from imports import *

testNoiseReduction = True
testCropping = False
makingGrid = False
makingCurveComparison = False
graph_dir = "C:/Users/AndyPC/Desktop/MagnetomorphsGithub/graphs/"

crop_29 = [130, 1200, 300, 2800]
image_array = ["29redBackground/DSC_00{} (3).JPG".format(i) for i in range(59, 68)]
currents_array = np.linspace(0, 4, 9)
bg_image = "29redBackground/DSC_0068 (3).JPG"
noise_reduction = [100, 210]
if makingGrid or makingCurveComparison:
    sample_array = [curvedPolmerSample(image, bg_image, crop_29, 2, current, noise_reduction) for image, current in
                    zip(image_array, currents_array)]

if testNoiseReduction:
    print("Making noise reduction test")
    rows, columns = 5, 5
    noise_test_sample_array = [curvedPolmerSample(image_array[0], bg_image, crop_29, 2, currents_array[0], [i, j],
                                                  displayText=False, text_size=5, display_data=False)
                               for i in np.linspace(10, np.mean(noise_reduction), rows)
                               for j in np.linspace(np.mean(noise_reduction), 230, columns)]
    fig, axs = plt.subplots(rows, columns)
    chi_squared_array = [noise_test_sample.redChiSq for noise_test_sample in noise_test_sample_array]
    chi_squared_mesh = np.reshape(chi_squared_array, (rows, columns))
    print("Making plot of model")
    for sample, ax in zip(noise_test_sample_array, axs.flat): sample.makePlotOfModel(ax)
    plt.show()
    x_mesh, y_mesh = np.meshgrid(np.linspace(10, np.mean(noise_reduction), rows + 1),
                                 np.linspace(np.mean(noise_reduction), 230, columns + 1))
    fig, ax0 = plt.subplots()
    ax0.set_xlabel("Lower Bound")
    ax0.set_ylabel("Upper Bound")
    cmap = plt.get_cmap('Purples')
    norm = mpl.colors.LogNorm(vmin=1, vmax=10)
    im = ax0.pcolormesh(x_mesh, y_mesh, chi_squared_mesh, cmap=cmap, norm=norm)
    cbar = fig.colorbar(im, ax=ax0, ticks=[1, 1.5, 2, 2.5, 3, 3.5, 4, 4, 5, 5, 6, 7, 8, 9, 10])
    cbar.ax.set_yticklabels(['1', ' 1.5', ' 2', ' 2.5', ' 3', ' 3.5', '4', '4', '5', '5', '6', '7', '8', '9', '10'])
    cbar.set_label('Reduced Chi Squared', rotation=270, labelpad=30)
    plt.show()
# making a grid plot to compare different currents
if makingGrid:
    fig, axs = plt.subplots(*(lambda c, t: (c, math.ceil(t / c)))(3, len(sample_array)))
    for sample, ax in zip(sample_array, axs.flat): sample.makePlotOfModel(ax)
    fig.canvas.manager.set_window_title('Test')
    mpl.rcParams["savefig.directory"] = graph_dir
    plt.show()
# making a comparison of models
if makingCurveComparison:
    fig, ax = plt.subplots()
    for sample in sample_array:
        sample.plot_errorbars(ax)
        sample.plot_model(ax)
    plt.legend()
    plt.show()
