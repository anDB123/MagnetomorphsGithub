from imports import *


class curvedPolmerSample:
    # properties of all dogs
    elastomer = "Silicone Elastomer"
    # initialize method
    scatter_worked = True
    x_data, y_data = [], []
    y_errors = []
    model_x_data, model_y_data = [], []
    difference_image = []
    noise_reduction_array = []
    start_of_curve = 0
    end_of_curve = 0
    curve_params = []
    model_bounds = []
    start_of_curve, end_of_curve, curve_params = 1600, 2000, [10000, 1800, 800]
    model_bounds = [[1, 0, 0], [np.inf, np.inf, np.inf]]
    model_used = "n_circ_fit"
    # fig, ax = plt.subplots()
    all_fitted_curves, all_fitted_params, limits_array = [], [], []
    redChiSq = -1

    def __init__(self, img_name, background_img_name, crop_array, thickness, current, difference_image_function,
                 noise_reduction_type, noise_reduction_array, number,
                 displayTextBool=True, text_size=5, display_data=False):
        self.img_name = img_name
        self.background_img_name = background_img_name
        self.crop_array = crop_array
        self.thickness = thickness
        self.current = current
        self.noise_reduction_array = noise_reduction_array
        self.displayTextBool = displayTextBool
        self.text_size = text_size
        self.display_data = display_data
        self.noise_reduction_type = noise_reduction_type
        self.difference_image_function = difference_image_function
        self.number = number
        self.analyseData()
        # self.makePlotOfModel()

    def reducedNoiseDifferenceImage(self):
        difference_image = self.difference_image_function(image_name=self.img_name,
                                                          background_name=self.background_img_name,
                                                          crop_array=self.crop_array)
        self.difference_image = self.noise_reduction_type(difference_image, *self.noise_reduction_array)

    def plotDifferenceImage(self, ax):
        ax.imshow(self.difference_image)

    def gaussian_averaging_of_y_data(self):
        temp_x_data, temp_y_data, temp_y_errors = [], [], []
        averaging_size = 20
        for i in range(averaging_size, len(self.x_data) - 2 * averaging_size):
            temp_x_data.append(self.x_data[i])
            gaussian_average = np.sum()
            temp_y_data.append(np.mean(self.y_data[i - averaging_size:i + averaging_size]))
            temp_y_errors.append(np.std(self.y_data[i - averaging_size:i + averaging_size]))
        self.x_data, self.y_data, self.y_errors = temp_x_data, temp_y_data, temp_y_errors

    def makeCurveFromDifferenceImage(self):
        try:
            self.x_data, self.y_data, self.y_errors = makeCurveFromDifferenceImage(self.difference_image)
            self.gaussian_averaging_of_y_data()

        except:
            print("Failed to make a scatter")
            self.scatter_worked = False
        if len(self.y_data) < 100:
            print("Too little data found")
            self.scatter_worked = False

    def linear_curve_linear_fit(self, ):
        self.model_x_data, self.model_y_data, a, b, model_fitted_params = modelTheCurve(self.x_data, self.y_data,
                                                                                        self.start_of_curve,
                                                                                        self.end_of_curve,
                                                                                        self.curve_params,
                                                                                        self.model_bounds)
        self.start_of_curve = a
        self.end_of_curve = b
        self.curve_params = model_fitted_params

    def n_curve_fit(self):
        init_vals = [10000, self.x_data[0], self.y_data[0]]
        circle_bounds = [[1, 0, 0], [np.inf, np.inf, np.inf]]
        self.curve_params = [circle_fit, init_vals, circle_bounds]
        self.all_fitted_curves, self.all_fitted_params, self.limits_array = n_curve_fit(self.x_data, self.y_data,
                                                                                        self.curve_params,
                                                                                        self.number)
        self.model_y_data = np.zeros(len(self.x_data))
        for i in range(len(self.limits_array) - 1):
            self.model_y_data[self.limits_array[i]:self.limits_array[i + 1]] = self.all_fitted_curves[i][1]

    def plot_n_curve_fit(self, ax):
        heat_colors, x_vals, y_vals = [], [], []
        for fitted_curve, params in zip(self.all_fitted_curves, self.all_fitted_params):
            heat_colors.append(params[0])
            x_vals.append(fitted_curve[0])
            y_vals.append(fitted_curve[1])
            ax.plot(fitted_curve[0], fitted_curve[1])
        heat_colors = [1 / heat_color for heat_color in heat_colors]
        heat_colors = heat_colors / np.max(heat_colors)  # normalize
        for i in range(len(x_vals)):
            ax.plot(x_vals[i], y_vals[i], color=(heat_colors[i], 0, 0))

    def findChiSquared(self):
        self.redChiSq = find_reduced_chi_squared(self.y_data, self.model_y_data, self.y_errors)

    def show_image(self, ax):
        ax.imshow(self.difference_image)

    def plot_errorbars(self, ax):
        ax.errorbar(self.x_data, self.y_data, yerr=self.y_errors, ls='none', label="Errorbars")

    def plot_model(self, ax):
        if self.model_used == "n_circ_fit":
            self.plot_n_curve_fit(ax)
        else:
            ax.plot(self.x_data, self.model_y_data, c='k', label="Model, I = {} A".format(self.current))

    def display_text(self, ax, x, y, text):
        ax.text(x, y, text,
                horizontalalignment='left', verticalalignment='top', transform=ax.transAxes,
                size=self.text_size,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

    def plotImageWithEdgesAndModel(self, ax):
        self.show_image(ax)
        if self.scatter_worked:
            self.plot_errorbars(ax)
            if self.model_used == "linear_curve_linear":
                self.plot_model()
            if self.model_used == "n_circ_fit":
                self.plot_n_curve_fit(ax)
        if self.display_data:
            display_data = "$ \chi ^2 _{red} = $" + "{:.2f}".format(
                self.redChiSq) + ", I = {}, noiseR = {},{},\ncrop = {},{},{},{}".format(self.current,
                                                                                        *self.noise_reduction_array,
                                                                                        *self.crop_array)
            self.display_text(ax, 0.05, 0.9, display_data)
        elif self.displayTextBool:
            ax.legend(loc='upper right', prop={'size': self.text_size})
            if self.scatter_worked:
                self.display_text(ax, 0.05, 0.9,
                                  "$ \chi ^2 _{red} = $" + "{:.2f}".format(self.redChiSq) + "\nCurrent = {} A".format(
                                      self.current))
            else:
                self.display_text(ax, 0.05, 0.9, "No Curve Found")

    def analyseData(self):
        self.reducedNoiseDifferenceImage()
        self.makeCurveFromDifferenceImage()
        if self.scatter_worked:
            if self.model_used == "linear_curve_linear":
                self.linear_curve_linear_fit()
            if self.model_used == "n_circ_fit":
                self.n_curve_fit()
            self.findChiSquared()

    def changeBlueOnlyNoiseReduction(self, noise_reduction_array):
        self.noise_reduction_array = noise_reduction_array
        self.analyseData()  # refreshes the plot
        return self

    def changeHSVNoiseReduction(self, noise_reduction_array):
        self.noise_reduction_array = noise_reduction_array
        self.analyseData()  # refreshes the plot
        return self

    def change_image_and_current(self, image, current):
        self.img_name = image
        self.current = current
        self.analyseData()
        return self


def make_sample_array(image_array, currents_array, initial_polymer_sample):
    sample_array = [initial_polymer_sample]
    for i in range(1, len(image_array)):
        start_time = time.time()
        temp_sample = copy.deepcopy(sample_array[i - 1])
        temp_sample.change_image_and_current(image_array[i], currents_array[i])
        sample_array.append(temp_sample)
        print("Time to make sample {} was {:.2f} seconds with chi squared of {:.2f}".format(i, time.time() - start_time,
                                                                                            temp_sample.redChiSq))
    return sample_array
