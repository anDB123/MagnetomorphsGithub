import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def create_blue_image(image_name):
    img = cv.imread(image_name)
    blue_img = img[:, :, 0]
    return blue_img
plt.imshow(create_blue_image("initial_curve_test/DSC_0061.JPG"))
plt.show()