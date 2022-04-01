from imports import *

testNoiseReduction = True
testCropping = True
bg_29 = "29redBackground/DSC_0068 (3).JPG"
im_array_29 = [
    "29redBackground/DSC_0067 (3).JPG",
    "29redBackground/DSC_0079 (3).JPG",
    "29redBackground/DSC_0090 (3).JPG",
    "29redBackground/DSC_0096 (3).JPG",
]
class curvedPolmerSample:
#properties of all dogs
    elastomer = "Silicone Elastomer"
#initialize method
    x_data , y_data = [], []
    model_x_data, model_y_data = [], []
    difference_image = []
    fig,ax = plt.subplots()
    def __init__(self, img_name, background_img_name, crop_array, thickness, current):
        self.img_name = img_name
        self.background_img_name = background_img_name
        self.crop_array = crop_array
        self.thickness = thickness
        self.current = current
        self.reducedNoiseDifferenceImage()
        self.makeCurveFromDifferenceImage()
        self.modelTheCurve()
        self.makePlotOfModel()
#instance methods
    # Instance method
    def getDifferenceImage(self):
        return makeDifferenceImage(image_name=self.img_name, background_name=self.background_img_name,crop_array=self.crop_array)
    def reducedNoiseDifferenceImage(self):
        self.difference_image = reduce_noise(self.getDifferenceImage(), 100, 170)
    def makeCurveFromDifferenceImage(self):
        self.x_data, self.y_data = makeCurveFromDifferenceImage(self.difference_image)
    def modelTheCurve(self):
        self.model_x_data, self.model_y_data =  modelTheCurve(self.x_data, self.y_data)
    def makePlotOfModel(self):
        self.ax.imshow(self.difference_image)
        self.ax.scatter(self.x_data, self.y_data)
        self.ax.plot(self.model_x_data, self.model_y_data, c='w')
        # displayPlots
        plt.show()
image = "29redBackground/DSC_0065 (3).JPG"
bg_image = "29redBackground/DSC_0068 (3).JPG"
crop_29 = [130, 1200, 300, 2700]
first_sample = curvedPolmerSample(image, bg_image, crop_29, 2, 1)