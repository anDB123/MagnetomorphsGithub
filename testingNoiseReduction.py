import scipy.stats

from edgeDetectionFunctions import *
from plottingFunctions import *
from deflectionCurveFitting.modelFunctions import *


def make_noise_comparison_grid(image_name, background_name, crop_array):
    cols = 5
    rows = 5
    counter = 1

    print("Working on " + image_name)
    img, bg, difference = create_difference_image(image_name, background_name,
                                                  crop_array)
    middle_val = 100
    a_min, a_max = 0, middle_val
    b_min, b_max = middle_val, 240
    for low_T in np.linspace(a_min, a_max, cols):
        for high_T in np.linspace(b_min, b_max, rows):
            try:
                ax = plt.subplot(rows, cols, counter)
                plt.xticks([])
                plt.yticks([])
                print("Testing for lowT = %d and highT = %d" % (low_T, high_T))
                low_noise_difference = reduce_noise(difference, low_T, high_T)
                plot_image(ax, low_noise_difference)
                print("finding edges...")
                edges_cv = find_edges_cv(low_noise_difference, 100, 200)
                edges_numpy = np.where(edges_cv == 255)
                x_edges, y_edges = get_edges_x_and_y_arrays(edges_numpy)
                ax.plot(x_edges, y_edges, label="Edges", linewidth=1, c='r')
                fit_params, covar_matrix = curve_fit(quadratic_fit, x_edges, y_edges, p0=quad_init_vals)
                ax.plot(x_edges, quadratic_fit(x_edges, *fit_params))
                chi_squared = scipy.stats.chisquare(f_obs=y_edges, f_exp=quadratic_fit(x_edges, *fit_params))[0]
                print("Chi Squared = {:.2f}".format(chi_squared))
                plt.legend(["Chi Squared = {:.2f}".format(chi_squared)])
                plt.title("lowT = %d and highT = %d" % (low_T, high_T))
            except:
                print("Edges not found")
            counter += 1
    plt.show()


background_name = "red_background_curve_test/DSC_0105.JPG"
image_name = "red_background_curve_test/DSC_0114.JPG"
crop_top, crop_bottom = 0, 2000
crop_left, crop_right = 0, 3000
crop_array = [crop_top, crop_bottom, crop_left, crop_right]
make_noise_comparison_grid(image_name, background_name, crop_array)
