import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl


def const_curve_angle_func(length, curvature_array):
    curvature_const = curvature_array[0]
    return length * curvature_const


def find_total_energy(angle_function, angle_func_init_array, number_of_arcs, properties_array):
    thickness, width, youngModulus, total_length, magnet_thickness, magnet_mass, magnet_strength, field_strength, density = properties_array
    arc_length = total_length / number_of_arcs
    x_array, y_array = np.zeros(number_of_arcs + 1), np.zeros(number_of_arcs + 1)
    all_lengths = np.linspace(0, total_length, number_of_arcs)
    all_angles = angle_function(all_lengths, angle_func_init_array)
    for current_angle, index in zip(all_angles, range(0, number_of_arcs)):
        x_array[index + 1] = x_array[index] + arc_length * np.cos(current_angle)
        y_array[index + 1] = y_array[index] + arc_length * np.sin(current_angle)

    magnetic_potential_energy = -1 / (4 * np.pi * 10 ** -7) * magnet_strength * magnet_thickness * np.pi * (
            magnet_thickness ** 2 / 4) * field_strength * np.sin(all_angles[-1])
    magnet_gravitational_energy = y_array[-1] * 9.81 * magnet_mass
    elastic_potential_energy = 0
    elastomer_graviational_energy = 0
    for height in y_array:
        elastomer_graviational_energy += density * thickness * width * arc_length * 9.81 * height
    for i in range(1, len(all_angles)):
        elastic_potential_energy += 1 / (4 * arc_length) * (youngModulus * thickness ** 3 * width) * \
                                    (all_angles[i] - all_angles[i - 1]) ** 3

    total_energy = magnetic_potential_energy + magnet_gravitational_energy + elastic_potential_energy + elastomer_graviational_energy

    energy_array = total_energy, magnetic_potential_energy, magnet_gravitational_energy, elastic_potential_energy, elastomer_graviational_energy
    return energy_array, x_array, y_array


def flat_then_const_curve_angle_func(length_array, curvature_array):
    curvature_const, curve_start = curvature_array
    returned_length_array = np.zeros(len(length_array))
    length_array = length_array - curve_start
    for i in range(len(length_array)):
        if length_array[i] >= 0:
            returned_length_array[i] = curvature_const * length_array[i]
    return returned_length_array


def test_angles_and_startpoints(num_angles_tested, num_startpoints_tested, max_angle, number_of_sections,
                                properties_array):
    max_length = properties_array[3]
    min_curved_length = 0.005
    angle_array = np.linspace(0, max_angle, num_angles_tested)
    startpoint_array = np.linspace(0, max_length - min_curved_length, num_startpoints_tested)
    curvature_bins = np.linspace(0, max_angle, num_angles_tested + 1)
    startpoint_bins = np.linspace(0, max_length - min_curved_length, num_startpoints_tested + 1)
    x, y = np.meshgrid(curvature_bins, startpoint_bins)
    a, b = np.meshgrid(angle_array, startpoint_array)
    z = np.zeros((num_angles_tested, num_startpoints_tested))

    for i in range(0, num_angles_tested):
        for j in range(0, num_startpoints_tested):
            startpoint = startpoint_array[j]
            curvature = angle_array[i] * np.pi / (180 * (max_length - startpoint))
            energies_array, flat_energy_x_array, flat_energy_y_array = find_total_energy(
                flat_then_const_curve_angle_func,
                [curvature, startpoint],
                number_of_sections, properties_array)
            z[i, j] = energies_array[0]
    print("The minimum energy is {}".format(np.min(z)))
    min_x, min_y = np.where(z == np.min(z))
    min_angle, min_startpoint = angle_array[min_x[0]], startpoint_array[min_y[0]]
    print("The values of minimum point is {}, {}".format(min_angle, min_startpoint))
    """
    fig, ax = plt.subplots()
    im = ax.pcolormesh(x, y, z.transpose())
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Energy', rotation=270, labelpad=30)
    ax.scatter(angle_array[min_x], startpoint_array[min_y], label="Minimum Point")
    ax.legend()
    plt.show()
    """
    return min_angle, min_startpoint


def test_curvature_angles(max_angle, startpoint, number_of_curves, properties_array, number_of_sections):
    angle_array = np.linspace(0, max_angle, number_of_curves)

    total_energies = np.zeros(number_of_curves)
    mag_potential_energies = np.zeros(number_of_curves)
    mag_gravity_energies = np.zeros(number_of_curves)
    elastic_potential_energies = np.zeros(number_of_curves)
    elastic_gravity_energies = np.zeros(number_of_curves)

    x_arrays = []
    y_arrays = []
    for i in range(0, number_of_curves):
        # print("Angle = {}".format(angle_array[i]))
        curvature = angle_array[i] / 180 * np.pi / (total_length - startpoint)
        energies_array, flat_energy_x_array, flat_energy_y_array = find_total_energy(flat_then_const_curve_angle_func,
                                                                                     [curvature, startpoint],
                                                                                     number_of_sections,
                                                                                     properties_array)
        x_arrays.append(flat_energy_x_array)
        y_arrays.append(flat_energy_y_array)
        total_energies[i], mag_potential_energies[i], mag_gravity_energies[i], elastic_potential_energies[i], \
        elastic_gravity_energies[i] = energies_array

    fig, ax = plt.subplots()
    ax.set_xlabel("X Values (m)")
    ax.set_ylabel("Y Values (m)")
    for x, y in zip(x_arrays, y_arrays):
        ax.plot(x, y)
    plt.show()
    fig, ax = plt.subplots()
    ax.set_xlabel("Final Angle (Degrees)")
    ax.set_ylabel("Energy (J)")
    ax.plot(angle_array, total_energies, label="Total Energy")
    ax.plot(angle_array, mag_potential_energies, label="Magnetic Potential Energy")
    ax.plot(angle_array, mag_gravity_energies, label="Magnetic Gravitational Energy")
    ax.plot(angle_array, elastic_potential_energies, label="Elastic Potential Energy")
    ax.plot(angle_array, elastic_gravity_energies, label="Elastomer Gravitational Potential Energy")
    ax.legend()
    plt.show()


def test_curvature_startpoints(fixed_angle, number_of_curves, properties_array, number_of_sections):
    startpoint_array = np.linspace(0, properties_array[3], number_of_curves)

    total_energies = np.zeros(number_of_curves)
    mag_potential_energies = np.zeros(number_of_curves)
    mag_gravity_energies = np.zeros(number_of_curves)
    elastic_potential_energies = np.zeros(number_of_curves)
    elastic_gravity_energies = np.zeros(number_of_curves)

    x_arrays = []
    y_arrays = []
    for i in range(0, number_of_curves):
        # print("Angle = {}".format(angle_array[i]))
        startpoint = startpoint_array[i]
        curvature = fixed_angle / 180 * np.pi / (total_length - startpoint)
        energies_array, flat_energy_x_array, flat_energy_y_array = find_total_energy(flat_then_const_curve_angle_func,
                                                                                     [curvature, startpoint],
                                                                                     number_of_sections,
                                                                                     properties_array)
        x_arrays.append(flat_energy_x_array)
        y_arrays.append(flat_energy_y_array)
        total_energies[i], mag_potential_energies[i], mag_gravity_energies[i], elastic_potential_energies[i], \
        elastic_gravity_energies[i] = energies_array

    fig, ax = plt.subplots()
    ax.set_xlabel("X Values (m)")
    ax.set_ylabel("Y Values (m)")
    for x, y in zip(x_arrays, y_arrays):
        ax.plot(x, y)
    plt.show()
    fig, ax = plt.subplots()
    ax.set_xlabel("Startpoint (m)")
    ax.set_ylabel("Energy (J)")
    ax.plot(startpoint_array, total_energies, label="Total Energy")
    ax.plot(startpoint_array, mag_potential_energies, label="Magnetic Potential Energy")
    ax.plot(startpoint_array, mag_gravity_energies, label="Magnetic Gravitational Energy")
    ax.plot(startpoint_array, elastic_potential_energies, label="Elastic Potential Energy")
    ax.plot(startpoint_array, elastic_gravity_energies, label="Elastomer Gravitational Potential Energy")
    ax.legend()
    plt.show()


thickness = 0.6 * 10 ** -3  # it was about 1 mm
width = 10 * 10 ** -3  # made to be exactly 1cm
youngModulus = 871931.69  # in pa found elsewhere in code
total_length = 60 * 10 ** -3  # around 6cm (this should not affect curve shape but will in this case)
magnet_thickness = 4 * 10 ** -3  # 4mm thick magnet
magnet_mass = 0.0005  # 1g magnet
magnet_strength = 0.4  # measured in tesla
field_strength = 6 * 10 ** - 3  # 6 mT as measured with gaussmeter
density = 1000  # assumed same as water

properties_array = [thickness, width, youngModulus, total_length, magnet_thickness, magnet_mass, magnet_strength,
                    field_strength, density]

test_curvature_angles(90, 0.03, 20, properties_array, 30)
test_curvature_startpoints(45, 20, properties_array, 30)
"""

def make_min_energy_curve(properties_array):
    min_angle, min_startpoint = test_angles_and_startpoints(100, 100, 90, 20, properties_array)
    min_curvature = min_angle * np.pi / 180 / (total_length - min_startpoint)
    energies_array, flat_energy_x_array, flat_energy_y_array = find_total_energy(flat_then_const_curve_angle_func,
                                                                                 [min_curvature, min_startpoint],
                                                                                 100,
                                                                                 properties_array)

    return flat_energy_x_array, flat_energy_y_array


fig, ax = plt.subplots()
for field_strength in np.linspace(0, 0.1, 30):
    properties_array[7] = field_strength
    flat_energy_x_array, flat_energy_y_array = make_min_energy_curve(properties_array)
    ax.plot(flat_energy_x_array, flat_energy_y_array, label=field_strength)
ax.set_xlim(-0.01, total_length + 0.01)
ax.set_ylim(-0.01, total_length + 0.01)
ax.set_title("Minimized Energy Curves")
ax.legend()
plt.show()
"""
