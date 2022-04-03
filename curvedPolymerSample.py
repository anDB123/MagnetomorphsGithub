import matplotlib.pyplot as plt

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
    # fig, ax = plt.subplots()
    redChiSq = -1


    def __init__(self, img_name, background_img_name, crop_array, thickness, current,
                 noise_reduction_array, start_of_curve, end_of_curve, curve_params,
                 displayText = True, text_size = 5, display_data=False):
        self.img_name = img_name
        self.background_img_name = background_img_name
        self.crop_array = crop_array
        self.thickness = thickness
        self.current = current
        self.noise_reduction_array = noise_reduction_array
        self.displayText = displayText
        self.reducedNoiseDifferenceImage()
        self.makeCurveFromDifferenceImage()
        self.text_size = text_size
        self.display_data = display_data
        self.start_of_curve = start_of_curve
        self.end_of_curve = end_of_curve
        self.curve_params = curve_params
        if self.scatter_worked:
            self.modelTheCurve()
            self.findChiSquared()
        # self.makePlotOfModel()

    # Instance method
    def getDifferenceImage(self):
        return makeDifferenceImage(image_name=self.img_name, background_name=self.background_img_name,
                                   crop_array=self.crop_array)

    def reducedNoiseDifferenceImage(self):
        self.difference_image = reduce_noise(self.getDifferenceImage(), *self.noise_reduction_array)

    def makeCurveFromDifferenceImage(self):
        try:
            self.x_data, self.y_data, self.y_errors = makeCurveFromDifferenceImage(self.difference_image)
        except:
            self.scatter_worked = False
        if len(self.y_data) < 100:
            self.scatter_worked = False

    def modelTheCurve(self):
        a, b = 1500, 2000
        init_params = 1500, 2000
        self.model_x_data, self.model_y_data, a, b, model_fitted_params = modelTheCurve(self.x_data, self.y_data,
                                                                                        self.start_of_curve, self.end_of_curve,
                                                                                        self.curve_params)
        self.start_of_curve = a
        self.end_of_curve = b
        self.curve_params = model_fitted_params

    def findChiSquared(self):
        self.redChiSq = find_reduced_chi_squared(self.y_data, self.model_y_data, self.y_errors)
    def show_image(self,ax): ax.imshow(self.difference_image)
    def plot_errorbars(self,ax): ax.errorbar(self.x_data, self.y_data, yerr=self.y_errors, ls='none', label="Errorbars")
    def plot_model(self,ax): ax.plot(self.model_x_data, self.model_y_data, c='k', label="Model, I = {} A".format(self.current))
    def makePlotOfModel(self, ax):
        self.show_image(ax)
        if self.scatter_worked:
            self.plot_errorbars(ax)
            self.plot_model(ax)
        if self.display_data:
            ax.text(0.05, 0.9,
                    "$ \chi ^2 _{red} = $" + "{:.2f}".format(self.redChiSq) + ", I = {}, noiseR = {},{},\ncrop = {},{},{},{}".format(self.current,*self.noise_reduction_array,*self.crop_array),
                    horizontalalignment='left',
                    verticalalignment='top', transform=ax.transAxes,
                    size=self.text_size,
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
        elif self.displayText:
            ax.legend(loc='upper right',prop={'size': self.text_size})
            if self.scatter_worked:
                ax.text(0.05, 0.9,
                        "$ \chi ^2 _{red} = $" + "{:.2f}".format(self.redChiSq) + "\nCurrent = {} A".format(self.current),
                        horizontalalignment='left',
                        verticalalignment='top', transform=ax.transAxes,
                        size= self.text_size,
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))
            else:
                ax.text(0.05, 0.9,
                        "No Curve Found",
                        horizontalalignment='left',
                        verticalalignment='top', transform=ax.transAxes,
                        size=self.text_size,
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

