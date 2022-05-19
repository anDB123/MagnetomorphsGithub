import copy

import numpy as np

from imports import *


class PhysicalModelManyCurvesGradient(PolymerModel):
    all_fitted_curves = None
    all_fitted_params = None
    limits_array = None
    model_x_data = None
    model_y_data = None
    curve_x_limits = []
    curve_y_limits = []
    energy_x_output_data = []
    energy_y_output_data = []

    def __init__(self, current, properties_array, initial_guesses):
        self.initial_guesses = initial_guesses
        self.current = current
        self.thickness, self.width, self.youngModulus, self.total_length, self.magnet_thickness, self.magnet_mass, self.magnet_strength, self.density = properties_array

    def update_current(self, new_current):
        self.current = new_current
        self.field_strength = self.current * 0.006 / 4

    def find_total_energy(self, angle_function, angle_func_init_array, energy_curve_resolution):
        arc_length = self.total_length / energy_curve_resolution
        x_array, y_array = np.zeros(energy_curve_resolution + 1), np.zeros(energy_curve_resolution + 1)
        all_lengths = np.linspace(0, self.total_length, energy_curve_resolution)
        all_angles = np.array(angle_function(all_lengths, angle_func_init_array))

        for current_angle, index in zip(all_angles, range(0, energy_curve_resolution)):
            x_array[index + 1] = x_array[index] + arc_length * np.cos(current_angle)
            y_array[index + 1] = y_array[index] + arc_length * np.sin(current_angle)

        heights_array = y_array - min(y_array)
        heights_array = np.abs(heights_array)

        magnetic_potential_energy = -1 / (4 * np.pi * 10 ** -7) * self.magnet_strength * \
                                    self.magnet_thickness ** 3 * np.pi / 4 * self.field_strength * \
                                    np.sin(all_angles[-1])
        magnet_gravitational_energy = heights_array[-1] * 9.81 * self.magnet_mass
        elastic_potential_energy = 0
        elastomer_graviational_energy = 0
        for height in heights_array:
            elastomer_graviational_energy += self.density * self.thickness * self.width * arc_length * 9.81 * height
        for i in range(1, len(heights_array) - 2):
            if heights_array[i] == min(heights_array): elastomer_graviational_energy *= 10
        for i in range(1, len(all_angles)):
            elastic_potential_energy += np.abs(
                1 / (4 * arc_length) * (self.youngModulus * self.thickness ** 3 * self.width) * \
                (all_angles[i] - all_angles[i - 1]) ** 3)
        total_energy = magnetic_potential_energy + elastic_potential_energy + elastomer_graviational_energy
        energy_array = total_energy, magnetic_potential_energy, magnet_gravitational_energy, elastic_potential_energy, elastomer_graviational_energy
        # print(f"\nEnergies = {energy_array}")
        """if all_angles[-1] < - np.pi / 2:
            return [1000000], [1], [1]"""

        return energy_array, x_array, y_array

    def many_curve_angle_func(self, length_array, curvature_array):
        num_of_curves = len(curvature_array)
        arc_length = length_array[-1] / num_of_curves
        arc_indexes = np.linspace(0, len(length_array), num_of_curves + 1)
        arc_indexes = [int(math.ceil(arc_index)) for arc_index in arc_indexes]
        angle_array = np.zeros(len(length_array))
        current_angle = 0
        for i in range(num_of_curves):
            for j in range(arc_indexes[i], arc_indexes[i + 1]):
                change_in_length = (arc_indexes[i + 1] - arc_indexes[i])
                angle_difference = curvature_array[i] * arc_length / change_in_length
                current_angle += angle_difference
                angle_array[j] = current_angle
        return angle_array

    def n_dimensional_energy_gradient(self, current_curvature_array, perturbation, energy_curve_resolution):
        energy_gradient_array = []
        current_energy, x_current, y_current = self.find_total_energy(self.many_curve_angle_func,
                                                                      current_curvature_array, energy_curve_resolution)
        perturbation_array = [perturbation] * len(current_curvature_array)
        for i in range(len(perturbation_array)):
            spread = 100
            max_temp_curvature_array = np.array(copy.deepcopy(current_curvature_array))
            max_temp_curvature_array = max_temp_curvature_array - perturbation_array[i] / (
                    2 * len(max_temp_curvature_array))
            max_temp_curvature_array[i] += perturbation_array[i]

            # if i + 1 < len(perturbation_array) - spread:
            #    max_temp_curvature_array[i + 1:i + spread] -= perturbation_array[i] / spread

            min_temp_curvature_array = np.array(copy.deepcopy(current_curvature_array))
            min_temp_curvature_array = min_temp_curvature_array + perturbation_array[i] / (
                    2 * len(min_temp_curvature_array))
            min_temp_curvature_array[i] -= perturbation_array[i]
            # if i + 1 < len(perturbation_array) - spread:
            #    min_temp_curvature_array[i + 1:i + spread] -= perturbation_array[i] / spread

            max_perturbed_energy, perturbed_x, perturbed_y = self.find_total_energy(self.many_curve_angle_func,
                                                                                    max_temp_curvature_array,
                                                                                    energy_curve_resolution)
            min_perturbed_energy, perturbed_x, perturbed_y = self.find_total_energy(self.many_curve_angle_func,
                                                                                    min_temp_curvature_array,
                                                                                    energy_curve_resolution)

            energy_gradient = (max_perturbed_energy[0] - min_perturbed_energy[0]) / (perturbation_array[i])
            energy_gradient_array.append(energy_gradient)
        # print(f"energy_gradient_array = {energy_gradient_array}")
        return energy_gradient_array

    def test_many_curvatures(self, curvature_testing_resolution, energy_curve_resolution):
        number_of_curves = len(self.initial_guesses)
        print(f"Testing {number_of_curves} curvatures")
        curvature_array = self.initial_guesses
        length_limits = np.linspace(0, self.total_length, len(curvature_array) + 1)
        continue_bool = True
        scaling_counter = 0

        delta_energy_difference_array = []
        energy_array = []
        # plt.ion()
        # figure, ax = plt.subplots()
        x_values, y_values = self.plot_curvature_model(curvature_array)
        # ax.set_title("Predicted Shape")
        # ax[1].set_title("Rate of improvement (change in energy)")
        # ax[2].set_title("Total Energy")
        # line1, = ax.plot(x_values, y_values)
        # line2, = ax[1].plot(x_values, y_values)
        # line3, = ax[2].plot(x_values, y_values)
        learning_rate = number_of_curves
        while continue_bool:
            current_energy, x, y = self.find_total_energy(self.many_curve_angle_func,
                                                          curvature_array,
                                                          energy_curve_resolution)
            gradient_array = np.array(
                self.n_dimensional_energy_gradient(curvature_array, 0.1, 100))

            new_curvature_array = curvature_array - gradient_array / np.linalg.norm(gradient_array) * learning_rate
            best_candidate_energy, best_x, best_y = self.find_total_energy(self.many_curve_angle_func,
                                                                           new_curvature_array,
                                                                           energy_curve_resolution)
            best_candidate_energy = best_candidate_energy[0]
            current_energy = current_energy[0]
            if scaling_counter > 100:
                continue_bool = False
            if best_candidate_energy < current_energy:
                energy_array.append(best_candidate_energy)
                new_curvature_array = np.array(new_curvature_array)
                # new_curvature_array = np.where(new_curvature_array < 0, new_curvature_array, 0)
                curvature_array = new_curvature_array

                new_energy_difference = current_energy - best_candidate_energy
                if scaling_counter > 1:
                    delta_energy_difference = np.abs(new_energy_difference - old_energy_difference)
                    delta_energy_difference_array.append(delta_energy_difference)
                    print(f"\rBest={best_candidate_energy:.4g}, Current={current_energy:.4g}, "
                          f"Energy difference= {new_energy_difference:.4g}, New Resolution = {curvature_testing_resolution:.4g}"
                          f", Iterations = {scaling_counter}",
                          end="")
                old_energy_difference = new_energy_difference
                scaling_counter += 1
            elif learning_rate > number_of_curves / (10 ** 5):
                learning_rate *= 0.1
            else:
                continue_bool = False
            x_array, y_array = self.plot_curvature_model(curvature_array)
            x_array = np.append(-x_array[::-1], x_array)
            y_array = np.append(y_array[::-1], y_array)
            # line1.set_xdata(x_array)
            # line1.set_ydata(y_array)
            # ax.set_ylim([-self.total_length, self.total_length])
            # ax.set_xlim([-self.total_length, self.total_length])
            # ax.set_aspect('equal')
            if scaling_counter > 3:
                x_vals = np.linspace(0, len(delta_energy_difference_array), len(delta_energy_difference_array))
                # ax[1].set_ylim([np.min(delta_energy_difference_array), np.max(delta_energy_difference_array)])
                # ax[1].set_xlim([0, len(delta_energy_difference_array)])
                # line2.set_xdata(x_vals)
                # line2.set_ydata(delta_energy_difference_array)
                # #ax[1].set_yscale("log")

                # line3.set_xdata(np.linspace(0, len(energy_array), len(energy_array)))
                # line3.set_ydata(energy_array)
                # axs[2].set_ylim([np.min(energy_array), np.max(energy_array)])
                # axs[2].set_xlim([0, len(energy_array)])
                # axs[2].set_yscale("log")

            # figure.canvas.draw()
            # figure.canvas.flush_events()
        energies_array, min_x_vals, min_y_vals = self.find_total_energy(self.many_curve_angle_func, curvature_array,
                                                                        energy_curve_resolution)
        print()
        print("The minimum energy curvatures are {}".format(curvature_array))
        # plt.ioff()
        # plt.close()
        return min_x_vals, min_y_vals, curvature_array

    def plot_curvature_model(self, curvatures):
        resolution = 100
        arc_length = self.total_length / (resolution)
        x_array, y_array = np.zeros(resolution + 1), np.zeros(resolution + 1)
        all_lengths = np.linspace(0, self.total_length, resolution)
        all_angles = self.many_curve_angle_func(all_lengths, curvatures)
        for current_angle, index in zip(all_angles, range(0, resolution)):
            x_array[index + 1] = x_array[index] + arc_length * np.cos(current_angle)
            y_array[index + 1] = y_array[index] + arc_length * np.sin(current_angle)

        return x_array, y_array

    def make_model_data(self, curvatures, curvature_length_limits, max_x):
        angle = 0
        current_l = 0
        current_y = 0
        self.curve_x_limits = []
        self.curve_y_limits = []
        # trying to map the length, angle function to x, y points for easy comparison.

        arc_length = 0
        curvature_index = 0
        current_curvature = curvatures[curvature_index]
        current_length_limit = curvature_length_limits[curvature_index + 1]
        previous_angle = 0
        self.model_x_data = np.linspace(0, max_x, len(self.x_data))
        self.model_y_data = [self.y_data[0]]
        for i in range(0, len(self.model_x_data) - 1):
            change_in_x = self.model_x_data[i + 1] - self.model_x_data[i]
            change_in_l = change_in_x / np.cos(angle)
            current_y += change_in_l * np.sin(angle)
            self.model_y_data.append(current_y)
            current_l += change_in_l
            arc_length += change_in_l
            angle = arc_length * current_curvature + previous_angle
            # print("Angle = {},Arc_length ={}, Length = {}, length limit = {}".format(angle, arc_length, current_l,
            #
            #                                                                         current_length_limit))
            if int(current_l) > int(current_length_limit):
                if (curvature_index + 1) < len(curvatures):
                    curvature_index += 1
                    current_curvature = curvatures[curvature_index]
                    current_length_limit = curvature_length_limits[curvature_index + 1]
                    arc_length = 0
                    self.curve_x_limits.append(self.model_x_data[i])
                    self.curve_y_limits.append(current_y)
                    previous_angle = angle
                    # print(f"l = {current_l}, curve = {current_curvature}")

    def fitModel(self, x_data, y_data):
        self.curve_y_limits = []
        self.curve_x_limits = []
        # remove front bit
        self.min_x_vals, self.min_y_vals, self.min_curvatures = self.test_many_curvatures(
            curvature_testing_resolution=10, energy_curve_resolution=200)
        x_offset = min(x_data)
        y_offset = np.mean(y_data[:5])  # 300 chosen as sample should be straight at beginning
        self.x_data = x_data - x_offset
        self.y_data = y_data - y_offset

        # trying to find curved_langth
        curved_length = 0
        leaps = 3

        for i in range(0, len(self.x_data) - leaps, leaps):
            x_length = self.x_data[i + leaps] - self.x_data[i]
            y_length = self.y_data[i + leaps] - self.y_data[i]
            curved_length += np.sqrt(x_length ** 2 + y_length ** 2)

        # modelled_length = self.total_length
        modelled_length = 0
        leaps = 1

        for i in range(0, len(self.min_x_vals) - leaps, leaps):
            x_length = self.min_x_vals[i + leaps] - self.min_x_vals[i]
            y_length = self.min_y_vals[i + leaps] - self.min_y_vals[i]
            modelled_length += np.sqrt(x_length ** 2 + y_length ** 2)

        scaling = curved_length / modelled_length
        self.scaling = scaling
        self.energy_x_output_data = [val * scaling for val in self.min_x_vals]
        self.energy_y_output_data = [val * scaling for val in self.min_y_vals]
        print("Scaling factor = {}".format(scaling))
        self.min_curvatures = [min_curvature / scaling for min_curvature in self.min_curvatures]

        self.curvature_length_limits = np.linspace(0, curved_length, len(self.min_curvatures) + 1)
        self.make_model_data(self.min_curvatures, self.curvature_length_limits, self.energy_x_output_data[-1])
        self.energy_x_output_data += x_offset
        self.energy_y_output_data = y_offset - self.energy_y_output_data
        self.model_x_data += x_offset
        self.model_y_data = y_offset - self.model_y_data  # this data is flipped
        self.curve_y_limits = y_offset - self.curve_y_limits
        self.curve_x_limits += x_offset
        self.model_x_data = np.array(self.model_x_data)
        self.model_y_data = np.array(self.model_y_data)
        print(f"Modelled arch Height = {(self.model_y_data[0] - self.model_y_data[-1]) / scaling * 1000} mm")

    def plotModel(self, ax):
        # ax.scatter(self.energy_x_output_data, self.energy_y_output_data, label="energy output", s=2, c='k')
        # ax.scatter(self.curve_x_limits, self.curve_y_limits, label="Curve Limits")
        ax.plot(self.model_x_data, self.model_y_data, label="Model data")
