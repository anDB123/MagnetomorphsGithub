from imports import *


class PhysicalModelManyCurves(PolymerModel):
    all_fitted_curves = None
    all_fitted_params = None
    limits_array = None
    model_x_data = None
    model_y_data = None
    curve_x_limits = []
    curve_y_limits = []
    energy_x_output_data = []
    energy_y_output_data = []

    def __init__(self, current, properties_array):

        self.current = current
        self.thickness, self.width, self.youngModulus, self.total_length, self.magnet_thickness, self.magnet_mass, self.magnet_strength, self.field_strength, self.density = properties_array

    def update_current(self, new_current):
        self.current = new_current
        self.field_strength = self.current * 0.006 / 4

    def find_total_energy(self, angle_function, angle_func_init_array, energy_curve_resolution):
        arc_length = self.total_length / energy_curve_resolution
        x_array, y_array = np.zeros(energy_curve_resolution + 1), np.zeros(energy_curve_resolution + 1)
        all_lengths = np.linspace(0, self.total_length, energy_curve_resolution)
        all_angles = angle_function(all_lengths, angle_func_init_array)
        for current_angle, index in zip(all_angles, range(0, energy_curve_resolution)):
            x_array[index + 1] = x_array[index] + arc_length * np.cos(current_angle)
            y_array[index + 1] = y_array[index] + arc_length * np.sin(current_angle)
        magnetic_potential_energy = -1 / (4 * np.pi * 10 ** -7) * self.magnet_strength * \
                                    self.magnet_thickness ** 3 * np.pi / 4 * self.field_strength * \
                                    np.sin(all_angles[-1])
        magnet_gravitational_energy = y_array[-1] * 9.81 * self.magnet_mass
        elastic_potential_energy = 0
        elastomer_graviational_energy = 0
        for height in y_array:
            elastomer_graviational_energy += self.density * self.thickness * self.width * arc_length * 9.81 * height
        for i in range(1, len(all_angles)):
            elastic_potential_energy += 1 / (4 * arc_length) * (self.youngModulus * self.thickness ** 3 * self.width) * \
                                        (all_angles[i] - all_angles[i - 1]) ** 3
        total_energy = magnetic_potential_energy + magnet_gravitational_energy + elastic_potential_energy + elastomer_graviational_energy
        energy_array = total_energy, magnetic_potential_energy, magnet_gravitational_energy, elastic_potential_energy, elastomer_graviational_energy
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
                angle_difference = curvature_array[i] * arc_length / (arc_indexes[i + 1] - arc_indexes[i])
                current_angle += angle_difference
                angle_array[j] = current_angle
        return angle_array

    def update_progress_bar(self, time_taken_array, i, j, k, l, m, curvature_testing_resolution):
        try:
            total_time = np.mean(time_taken_array) * curvature_testing_resolution ** 5
            if (total_time == 0):
                print(f"\r Total time estimate = 0", end="")
            else:
                estimated_time_remaining = np.mean(time_taken_array) * (
                    (
                            curvature_testing_resolution ** 5 - i * curvature_testing_resolution ** 4 - j * curvature_testing_resolution ** 3 - k * curvature_testing_resolution ** 2 - l * curvature_testing_resolution - m))
                fraction = estimated_time_remaining / total_time
                total_length = 50

                bar = '???' * int(math.ceil(50 * (1 - fraction))) + int(
                    math.floor((total_length * fraction))) * '-'
                print(
                    f"\r {bar} {(1 - fraction) * 100:.1f}% Finished,  Estimated time remaining = {estimated_time_remaining:.0f}/{total_time:.0f}s",
                    end="")
        except:
            print(f"\r temp failure to calculate percentage", end="")

    def test_five_curvatures(self, min_curvature, max_curvature, curvature_testing_resolution,
                             energy_curve_resolution):
        individual_curvature_array = np.linspace(min_curvature, max_curvature, curvature_testing_resolution)
        arc_length = self.total_length / 5
        print("Testing 5 curvatures")
        z = np.zeros(([curvature_testing_resolution] * 5))  # this is a 5-dimensional_array
        time_taken_array = []
        for i in range(curvature_testing_resolution):
            for j in range(curvature_testing_resolution):
                for k in range(curvature_testing_resolution):
                    for l in range(curvature_testing_resolution):
                        for m in range(curvature_testing_resolution):
                            start_time = time.time()
                            curvatures_array = individual_curvature_array[i], individual_curvature_array[j], \
                                               individual_curvature_array[k], individual_curvature_array[l], \
                                               individual_curvature_array[m]
                            energies_array, flat_energy_x_array, flat_energy_y_array = self.find_total_energy(
                                self.many_curve_angle_func, curvatures_array, energy_curve_resolution)
                            z[i, j, k, l, m] = energies_array[0]
                            time_taken_array.append(time.time() - start_time)
                            self.update_progress_bar(time_taken_array, i, j, k, l, m, curvature_testing_resolution)
        print()
        print("The minimum energy is {}".format(np.min(z)))
        min_i, min_j, min_k, min_l, min_m = np.where(z == np.min(z))
        min_curvatures = [individual_curvature_array[min_i[0]], individual_curvature_array[min_j[0]],
                          individual_curvature_array[min_k[0]], individual_curvature_array[min_l[0]],
                          individual_curvature_array[min_m[0]]]
        energies_array, min_x_vals, min_y_vals = self.find_total_energy(
            self.many_curve_angle_func,
            min_curvatures,
            energy_curve_resolution)
        print("The minimum energy curvatures are {}".format(min_curvatures))
        return min_x_vals, min_y_vals, min_curvatures

    def make_model_data(self):
        angle = 0
        current_l = 0
        current_y = 0
        self.model_x_data = [0]
        self.model_y_data = [0]
        # trying to map the length, angle function to x, y points for easy comparison.

        arc_length = 0
        curvature_index = 0
        current_curvature = self.min_curvatures[curvature_index]
        current_length_limit = self.curvature_length_limits[curvature_index + 1]
        previous_angle = 0
        for i in range(0, len(self.x_data) - 1):
            change_in_x = self.x_data[i + 1] - self.x_data[i]
            change_in_l = change_in_x / np.cos(angle)
            current_y += change_in_l * np.sin(angle)
            self.model_x_data.append(self.x_data[i])
            self.model_y_data.append(current_y)
            current_l += change_in_l
            arc_length += change_in_l
            angle = arc_length * current_curvature + previous_angle
            # print("Angle = {},Arc_length ={}, Length = {}, length limit = {}".format(angle, arc_length, current_l,
            #                                                                         current_length_limit))
            if int(current_l) > int(current_length_limit):
                if (curvature_index + 1) < 5:
                    curvature_index += 1
                    current_curvature = self.min_curvatures[curvature_index]
                    current_length_limit = self.curvature_length_limits[curvature_index + 1]
                    arc_length = 0
                    self.curve_x_limits.append(self.x_data[i])
                    self.curve_y_limits.append(current_y)
                    previous_angle = angle

    def fitModel(self, x_data, y_data):
        self.curve_y_limits = []
        self.curve_x_limits = []
        self.min_x_vals, self.min_y_vals, self.min_curvatures = self.test_five_curvatures(0, 20, 5, 100)
        x_offset = min(x_data)
        y_offset = np.mean(y_data[:300])  # 300 chosen as sample should be straight at beginning
        self.x_data = x_data - x_offset
        self.y_data = y_data - y_offset
        output_length = max(x_data) - min(x_data)
        modelled_length = self.total_length
        scaling = output_length / modelled_length
        self.energy_x_output_data = [val * scaling + x_offset for val in self.min_x_vals]
        self.energy_y_output_data = [y_offset - val * scaling for val in self.min_y_vals]

        print("Scaling factor = {}".format(scaling))
        self.min_curvatures = [min_curvature / scaling for min_curvature in self.min_curvatures]
        # trying to find curved_langth
        curved_length = 0
        leaps = 5

        for i in range(0, len(x_data) - leaps, leaps):
            x_length = x_data[i + leaps] - x_data[i]
            y_length = y_data[i + leaps] - y_data[i]
            curved_length += np.sqrt(x_length ** 2 + y_length ** 2)

        self.curvature_length_limits = np.linspace(0, curved_length, 6)
        self.make_model_data()

        self.model_x_data += x_offset
        self.model_y_data = y_offset - self.model_y_data  # this data is flipped
        self.curve_y_limits = y_offset - self.curve_y_limits
        self.model_x_data = np.array(self.model_x_data)
        self.model_y_data = np.array(self.model_y_data)

    def plotModel(self, ax):
        ax.plot(self.model_x_data, self.model_y_data, label="Model data")
        # ax.scatter(self.curve_x_limits, self.curve_y_limits, label="Curve Limits")
        ax.scatter(self.energy_x_output_data, self.energy_y_output_data, label="energy output", s=2)
