import numpy as np
import cv2 as cv

def create_blue_image(image_name):
    img = cv.imread(image_name)
    blue_img = img[:, :, 0]
    return blue_img