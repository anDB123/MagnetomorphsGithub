import matplotlib.pyplot as plt

from imports import *


class PhysicalModel(PolymerModel):
    all_fitted_curves = None
    all_fitted_params = None
    limits_array = None
    model_x_data = None
    model_y_data = None

    def __init__(self, current, thickness, width, youngModulus, total_length, magnet_thickness, magnet_mass,
                 magnet_strength, density):
        self.current = current
        self.thickness = thickness
        self.width = width
        self.youngModulus = youngModulus
        self.total_length = total_length
        self.magnet_thickness = magnet_thickness
        self.magnet_mass = magnet_mass
        self.magnet_strength = magnet_strength
        self.density = density
        self.field_strength = current * 0.0015
        self.properties_array = [self.thickness, self.width, self.youngModulus, self.total_length,
                                 self.magnet_thickness, self.magnet_mass, self.magnet_strength, self.field_strength,
                                 density]

    def update_current(self, new_current):
        self.current = new_current
        self.properties_array[7] = self.current * 0.0015

    def find_total_energy(self, angle_function, angle_func_init_array, number_of_arcs, properties_array):
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

    def flat_then_const_curve_angle_func(self, length_array, curvature_array):
        curvature_const, curve_start = curvature_array
        returned_angle_array = np.zeros(len(length_array))
        length_array = length_array - curve_start
        for i in range(len(length_array)):
            if length_array[i] >= 0:
                returned_angle_array[i] = curvature_const * length_array[i]
        return returned_angle_array

    def test_angles_and_startpoints(self, num_angles_tested, num_startpoints_tested, max_angle, number_of_sections,
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
                energies_array, flat_energy_x_array, flat_energy_y_array = self.find_total_energy(
                    self.flat_then_const_curve_angle_func,
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
        ax.set_xlabel("Deflection Angle (degrees)")
        ax.set_ylabel("Deflection start point (m)")
        plt.show()
        """
        return min_angle, min_startpoint

    def make_min_energy_curve(self):
        min_angle, min_startpoint = self.test_angles_and_startpoints(100, 100, 90, 20, self.properties_array)
        min_curvature = min_angle * np.pi / 180 / (self.total_length - min_startpoint)
        energies_array, flat_energy_x_array, flat_energy_y_array = self.find_total_energy(
            self.flat_then_const_curve_angle_func,
            [min_curvature, min_startpoint],
            100,
            self.properties_array)

        return flat_energy_x_array, flat_energy_y_array

    def fitModel(self, x_data, y_data):
        min_angle, min_startpoint = self.test_angles_and_startpoints(100, 100, 90, 20, self.properties_array)
        min_angle = min_angle * np.pi / 180
        x_offset = min(x_data)

        x_data = x_data - x_offset

        output_length = max(x_data)
        modelled_length = self.total_length
        scaling = output_length / modelled_length
        min_startpoint = min_startpoint * scaling
        print("output length = {}, min_startpoint = {}".format(output_length, min_startpoint))
        curved_iterations = int(math.ceil(output_length - min_startpoint))
        curved_length = 0
        # y_offset = np.mean(y_data[:-curved_iterations])
        y_offset = np.mean(y_data[:-curved_iterations])
        for x, angle in zip(np.linspace(1, 1, curved_iterations), np.linspace(0, min_angle, curved_iterations)):
            curved_length += x / np.cos(angle)
        print("max_angle - {}, curved_length = {}".format(min_angle, curved_length))
        angle = 0
        current_l = 0
        current_y = 0
        self.model_x_data = x_data
        self.model_y_data = []
        for i in range(len(x_data)):
            if x_data[i] < min_startpoint:
                self.model_y_data.append(0)
            else:
                change_in_x = x_data[i] - x_data[i - 1]
                change_in_l = change_in_x / np.cos(angle)
                current_l = current_l + change_in_l
                angle = current_l / (curved_length) * min_angle
                print("X_value = {}, Delta x = {}, delta l = {}, current_length = {}, angle = {}".format(x_data[i],
                                                                                                         change_in_x,
                                                                                                         change_in_l,
                                                                                                         current_l,
                                                                                                         angle))
                current_y = current_y + change_in_l * np.sin(angle)
                self.model_y_data.append(current_y)
        self.model_x_data += x_offset
        self.model_y_data = y_offset - self.model_y_data
        self.model_x_data = np.array(self.model_x_data)
        self.model_y_data = np.array(self.model_y_data)

    def plotModel(self, ax):
        ax.plot(self.model_x_data, self.model_y_data, label="Model data")
