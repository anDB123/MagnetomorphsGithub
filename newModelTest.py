from edgeDetectionFunctions import *
from fitting_code import *


def find_magnetic_potential(x, theta, length, bFieldStrength, magnetStrength):
    # function to find potential energy for a permanent dipole magnet in a uniform field
    return 2 * x * length * np.sin(theta) * bFieldStrength * magnetStrength


def find_arc(radius, angle):
    # finds arclength.
    # radius in any unit
    # angle in radians
    return angle * radius


def find_strain(unstretched_length, stretched_length):
    # finds strain as deltaL/L
    return (stretched_length - unstretched_length) / unstretched_length


def circular_deflection_delta_strain(radius, angle, inside_radius, outside_radius):
    inside_arc = find_arc(inside_radius, angle)
    outside_arc = find_arc(outside_radius, angle)
    middle_arc = find_arc(radius, angle)
    # y=mx+c integral
    outside_max_strain = find_strain(middle_arc, outside_arc)
    inside_max_strain = find_strain(middle_arc, inside_arc)
    total_inside_strain = 1 / 2 * inside_max_strain * (inside_radius - radius)
    total_outside_strain = 1 / 2 * outside_max_strain * (outside_radius - radius)
    total_arc_strain = total_inside_strain + total_outside_strain
    return total_arc_strain


def find_elastic_energy(length, radius):
    angle = length / radius
    thickness = 100
    width = 1000
    youngsModulus = 871931.69
    area = thickness * width
    absStrain = circular_deflection_delta_strain(radius, angle, radius - thickness / 2, radius + thickness / 2)
    energy = strain * youngsModulus * area / length


def find_total_curve_strain(x_values, y_max_vals, y_min_vals):
    for i in range(len(x_values)):
        y_min_data = y_min_vals[i:i + 2]
        y_max_data = y_max_vals[i:i + 2]
        x_data = x_values[i:i + 2]
    # should fit curve here
    return 0


def find_bending_elastic_potential():
    # finds the potential energy due to bending in a polymer
    """height, width, length, young's modulus, x_data, top_y_data, bot_y_data
    loop through data to find b ending found in data points.
    Then use numerical integration to find many small circular sections and so stretching criteria"""

    return 0


def physicalModelFunction():
    """
    mass_of_magnet
    length of magnet
    mass of polymer
    young's modulus
    uniform field strength
    magnet field strength
    contact point with surface
    length of bend
    width of polymer

    returns y values based on x values
    """
    x = 0
    return x


def get_x_and_y_data_from_image(image_name, background_name, crop_array):
    low_t, high_t = 100, 170
    img, bg, difference = create_difference_image(image_name, background_name, crop_array)
    low_noise_difference = reduce_noise(difference, low_t, high_t)
    x_edges, y_edges, y_edges_error = get_edges(low_noise_difference)
    return x_edges, y_edges, y_edges_error


def make_array_image_comparison_reference(image_array, background_name, crop_array, x_values, model_array, trim_end):
    # function to generate difference image, find edges, find centre between edges, model centres and plot the result
    cols = 3
    rows = math.ceil(len(image_array) / cols)
    counter = 1
    low_t, high_t = 100, 170
    initial_a, initial_b = 1100.0, 1600.0
    deflection_curves, deflection_fits, chi_squareds = [], [], []
    for image_name in image_array:
        # Keeping track of progress
        print("Working on " + image_name)
        print("Fitting with {}".format(model_array[0]))
        # using open cv to make image arrays
        img, bg, difference = create_difference_image(image_name, background_name, crop_array)

        x_edges, y_edges, y_edges_error = get_x_and_y_data_from_image(image_name, background_name, crop_array)
        x_edges, y_edges, y_edges_error = x_edges[:-trim_end], y_edges[:-trim_end], y_edges_error[:-trim_end]
        # fitting
        x_model_array, y_model_array, a, b, current_params = model_array[0](x_edges, y_edges, *model_array[1])
        model_array[1][2][1] = current_params
        # find reduced chi squared
        reduced_chi_squared = find_reduced_chi_squared(y_edges, y_model_array, y_edges_error)
        chi_squared_label = "I = {}A, $\chi_r^2$ = {:.2f}".format(x_values[counter - 1], reduced_chi_squared)
        # Plotting
        ax = plt.subplot(rows, cols, counter)
        plot_image_with_fit(ax, img, x_edges, y_edges, x_model_array, y_model_array, chi_squared_label,
                            a, b)
        # appending arrays
        deflection_curves.append([x_edges, y_edges])
        deflection_fits.append([x_model_array, y_model_array])
        chi_squareds.append(chi_squared_label)
        counter += 1
    plt.tight_layout()
    plt.show()
    # making new subplot
    ax = plt.subplot()
    for i in range(len(deflection_curves)):
        # making deflection curves with the modelled fit
        x, y = deflection_curves[i]
        model_x, model_y = deflection_fits[i]
        ax.scatter(x, y, label=chi_squareds[i])
        ax.plot(model_x, model_y, c='k')
    ax.invert_yaxis()
    plt.legend()

    plt.show()


def test_model_initially(x_data, y_data, model_array):
    plt.plot(x_data, y_data, label="data")
    plt.plot(x_data, model_array[0](x_data, *model_array[1]))
    plt.show()


def show_differrence_image(image_name, background_name, crop_array):
    img, bg, difference = create_difference_image(image_name, background_name, crop_array)
    plt.imshow(difference)
    plt.show()
    difference = reduce_noise(difference, 100, 170)
    plt.imshow(difference)
    plt.show()


"""
background_name = "initial_curve_test/DSC_0069.JPG"
image_array = []
for i in range(0, 9): image_array.append("initial_curve_test/DSC_006{}.JPG".format(i))
crop_top, crop_bottom = 500, 1250
crop_left, crop_right = 0, 3000
crop_array = [crop_top, crop_bottom, crop_left, crop_right]
current_values = [0.000, 0.512, 0.999, 1.506, 2.030, 2.499, 2.997, 3.508, 3.975]
model = linear_curve_linear_fit
x_edges, y_edges, y_edges_error = get_x_and_y_data_from_image("initial_curve_test/DSC_0068.JPG", "initial_curve_test/DSC_0069.JPG", crop_array)
circle_test_array = [circle_fit,[1200,1600,450]]
test_model_initially(x_edges, y_edges, circle_test_array)

linear_curve_linear_model_array = [linear_curve_linear_fit, [1300.0, 2400.0,circle_test_array]]

make_array_image_comparison_reference(image_array, background_name, crop_array, current_values, linear_curve_linear_model_array, 80)

"""

background_name = "29redBackground/DSC_0068 (3).JPG"
image_array = []
for i in range(59, 68): image_array.append("29redBackground/DSC_00{} (3).JPG".format(i))
crop_top, crop_bottom = 500, 1250
crop_left, crop_right = 0, 3000
crop_array = [crop_top, crop_bottom, crop_left, crop_right]
current_values = [0.000, 0.512, 0.999, 1.506, 2.030, 2.499, 2.997, 3.508, 3.975]
model = linear_curve_linear_fit
x_edges, y_edges, y_edges_error = get_x_and_y_data_from_image("29redBackground/DSC_0067 (3).JPG", background_name,
                                                              crop_array)
circle_test_array = [circle_fit, [1200, 1600, 450]]
test_model_initially(x_edges, y_edges, circle_test_array)

show_differrence_image("29redBackground/DSC_0059 (3).JPG", background_name, crop_array)

linear_curve_linear_model_array = [linear_curve_linear_fit, [1300.0, 2400.0, circle_test_array]]

make_array_image_comparison_reference(image_array, background_name, crop_array, current_values,
                                      linear_curve_linear_model_array, 80)
