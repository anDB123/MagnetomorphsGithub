import matplotlib.pyplot as plt

from imports import *


class DifferenceImageObject:
    def __init__(self, img_name, background_img_name, crop_array, difference_image_function,
                 noise_reduction_type, noise_reduction_array):
        self.difference_image = None
        self.img_name = img_name
        self.background_img_name = background_img_name
        self.crop_array = crop_array
        self.difference_image_function = difference_image_function
        self.noise_reduction_type = noise_reduction_type
        self.noise_reduction_array = noise_reduction_array
        self.reducedNoiseDifferenceImage()

    def reducedNoiseDifferenceImage(self):
        difference_image = self.difference_image_function(image_name=self.img_name,
                                                          background_name=self.background_img_name,
                                                          crop_array=self.crop_array)
        self.difference_image = self.noise_reduction_type(difference_image, self.noise_reduction_array)

    def show_difference_image(self, ax):
        ax.imshow(self.difference_image)

    def changeHSVNoiseReduction(self, noise_reduction_array):
        self.noise_reduction_array = noise_reduction_array
        self.reducedNoiseDifferenceImage()

    def replaceImage(self, new_image_name):
        self.img_name = new_image_name
        self.reducedNoiseDifferenceImage()

    def show_colour_diff_img(self):
        img = cv.imread(self.img_name)
        lowR, highR = [0, 255]
        lowG, highG = [0, 255]
        lowB, highB = [20, 240]
        b_mask = cv.inRange(img, (lowB, 0, 0), (highB, 255, 255))
        g_mask = cv.inRange(img, (0, lowG, 0), (255, highG, 255))
        r_mask = cv.inRange(img, (0, 0, lowR), (255, 255, highR))
        masks = [b_mask, g_mask, r_mask]
        fig, axs = plt.subplots(3, 2)
        for color_index, color_name in zip([0, 1, 2], ["Blue", "Green", "Red"]):
            axs[color_index, 0].imshow(img[:, :, color_index])
            axs[color_index, 0].set_title("{} channel original image".format(color_name))
            filtered_image = cv.bitwise_and(img, img, mask=masks[color_index])
            axs[color_index, 1].imshow(filtered_image[:, :, color_index])
            axs[color_index, 1].set_title("{} channel filtered image".format(color_name))
        plt.show()

        bg = cv.imread(self.background_img_name)
        difference = img - bg
        plt.imshow(difference)
        plt.show()
        plt.imshow(difference[:, :, 0])
        plt.title("Blue channel Only")
        plt.show()


class PolymerSample:
    elastomer = "Silicone Elastomer"

    def __init__(self, thickness, current):
        self.thickness = thickness
        self.current = current


class PolymerModel:
    model_x_data = None
    model_y_data = None

    def fitModel(self, x_data, y_data):
        self.model_x_data = x_data
        self.model_y_data = y_data

    def plotModel(self, ax):
        return

    def update_current(self, new_current):
        return


class NCurveModel(PolymerModel):
    all_fitted_curves = None
    all_fitted_params = None
    limits_array = None
    model_x_data = None
    model_y_data = None

    def __init__(self, curve_params, number):
        self.curve_params = curve_params
        self.number = number

    def fitModel(self, x_data, y_data):
        init_vals = [10000, x_data[0], y_data[0]]
        circle_bounds = [[1, 0, 0], [np.inf, np.inf, np.inf]]
        self.curve_params = [circle_fit, init_vals, circle_bounds]
        self.all_fitted_curves, self.all_fitted_params, self.limits_array = n_curve_fit(x_data, y_data,
                                                                                        self.curve_params,
                                                                                        self.number)
        self.model_x_data = x_data
        self.model_y_data = np.zeros(len(x_data))
        for i in range(len(self.limits_array) - 1):
            self.model_y_data[self.limits_array[i]:self.limits_array[i + 1]] = self.all_fitted_curves[i][1]

    def plotModel(self, ax):
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


class LinearCurveLinearModel(PolymerModel):
    model_x_data = None
    model_y_data = None

    def __init__(self, start_of_curve, end_of_curve, curve_params, model_bounds, current):
        self.current = current
        self.start_of_curve, self.end_of_curve, self.curve_params, self.model_bounds = start_of_curve, end_of_curve, curve_params, model_bounds

    def fitModel(self, x_data, y_data):
        self.model_x_data, self.model_y_data, self.start_of_curve, self.end_of_curve, self.curve_params = \
            modelTheCurve(x_data, y_data, self.start_of_curve, self.end_of_curve, self.curve_params,
                          self.model_bounds)

    def plotModel(self, ax):
        ax.plot(self.model_x_data, self.model_y_data, c='k', label="Model, I = {} A".format(self.current))


class PolymerPlotMethods:
    def gaussian_averaging_of_y_data(self):
        temp_x_data, temp_y_data, temp_y_errors = [], [], []
        averaging_size = 20
        for i in range(averaging_size, len(self.x_data) - 2 * averaging_size):
            temp_x_data.append(self.x_data[i])
            temp_y_data.append(np.mean(self.y_data[i - averaging_size:i + averaging_size]))
            y_error = 10
            # temp_y_errors.append(np.std(self.y_data[i - averaging_size:i + averaging_size]))
            temp_y_errors.append(y_error)
        temp_x_data, temp_y_data = temp_x_data, temp_y_data
        self.x_data, self.y_data, self.y_errors = temp_x_data, temp_y_data, temp_y_errors

    def makeCurveFromDifferenceImage(self):
        self.x_data, self.y_data, self.y_errors = makeCurveFromDifferenceImage(
            self.difference_image_obj.difference_image, 100, 200, 3)
        self.x_data, self.y_data, self.y_errors = self.x_data[50:-30], self.y_data[50:-30], self.y_errors[50:-30]
        # rotation to conpensate for sample
        self.gaussian_averaging_of_y_data()
        self.scatter_worked = True
        if len(self.y_data) < 100:
            print("Too little data found")
            self.scatter_worked = False
        # split_down_middle
        middle_point = int(np.mean(self.x_data)) - int(np.min(self.x_data))
        self.x_data, self.y_data, self.y_errors = self.x_data[middle_point:], self.y_data[middle_point:], self.y_errors[
                                                                                                          middle_point:]

    def findChiSquared(self):
        self.redChiSq = find_reduced_chi_squared(self.y_data, self.shapeFitModel.model_y_data, self.y_errors)

    def plot_errorbars(self, ax):
        ax.errorbar(self.x_data, self.y_data, yerr=self.y_errors, ls='none', label="Errorbars")

    def plot_model(self, ax):
        self.shapeFitModel.plotModel(ax)

    def display_text(self, ax, x, y, text):
        ax.text(x, y, text,
                horizontalalignment='left', verticalalignment='top', transform=ax.transAxes,
                size=self.text_size,
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

    def plotImageWithEdgesAndModel(self, ax):
        self.difference_image_obj.show_difference_image(ax)
        if self.scatter_worked:
            self.plot_errorbars(ax)
            self.shapeFitModel.plotModel(ax)
        if self.display_data:
            display_data = "$ \chi ^2 _{red} = $" + "{:.2f}".format(
                self.redChiSq) + ", I = {}, noiseR = {},{},\ncrop = {},{},{},{}".format(self.polymerSample.current,
                                                                                        *self.noise_reduction_array,
                                                                                        *self.crop_array)
            self.display_text(ax, 0.05, 0.9, display_data)
        elif self.displayTextBool:
            ax.legend(loc='upper right', prop={'size': self.text_size})
            if self.scatter_worked:
                self.display_text(ax, 0.05, 0.9,
                                  "$ \chi ^2 _{red} = $" + "{:.2f}".format(self.redChiSq) + "\nCurrent = {} A".format(
                                      self.polymerSample.current))
            else:
                self.display_text(ax, 0.05, 0.9, "No Curve Found")

    def analyseData(self):
        self.makeCurveFromDifferenceImage()
        if self.scatter_worked:
            self.shapeFitModel.fitModel(self.x_data, self.y_data)
            self.findChiSquared()


class CurvedPolymerSample(PolymerSample, PolymerPlotMethods):
    model_bounds = [[1, 0, 0], [np.inf, np.inf, np.inf]]
    model_used = "n_circ_fit"
    all_fitted_curves, all_fitted_params, limits_array = [], [], []
    redChiSq = -1

    def __init__(self, difference_image_obj, polymerSample, number, shapeFitModel,
                 displayTextBool=True, text_size=5, display_data=False):
        self.polymerSample = polymerSample
        self.difference_image_obj = difference_image_obj
        self.displayTextBool = displayTextBool
        self.text_size = text_size
        self.display_data = display_data
        self.number = number
        self.shapeFitModel = shapeFitModel
        self.analyseData()

    def change_diff_image_and_current(self, image, current):
        self.difference_image_obj.replaceImage(image)
        self.polymerSample.current = current
        self.shapeFitModel.update_current(current)
        self.analyseData()


def make_sample_array(image_array, currents_array, initial_polymer_sample):
    sample_array = [initial_polymer_sample]
    for i in range(1, len(image_array)):
        start_time = time.time()
        temp_sample = copy.deepcopy(sample_array[i - 1])
        temp_sample.change_diff_image_and_current(image_array[i], currents_array[i])
        sample_array.append(temp_sample)
        print("Time to make sample {} was {:.2f} seconds with chi squared of {:.2f}".format(i, time.time() - start_time,
                                                                                            temp_sample.redChiSq))
    return sample_array
