import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import scipy.stats

def get_edges_x_and_y_arrays(edges_np):
    x_unique = np.unique(edges_np[1])
    x_array = np.empty((0, 1))
    y_array = np.empty((0, 1))
    for x_value in x_unique:
        x_indices = np.where(x_value == edges_np[1])
        y_values = edges_np[0][x_indices]
        if np.size(y_values) >= 2:
            y_values = [y_values[0], y_values[-1]]
            x_array = np.append(x_array, x_value)
            y_array = np.append(y_array, np.mean(y_values))
    return x_array, y_array



def find_edges(difference):
    return cv.Canny(difference, 100, 200)


def create_difference_image(image_name, background_name, crop_array):
    crop_top, crop_bottom, crop_left, crop_right = crop_array

    img = cv.imread(image_name)

    bg = cv.imread(background_name)

    img = img[crop_top:crop_bottom, crop_left:crop_right]
    bg = bg[crop_top:crop_bottom, crop_left:crop_right]
    blue_img = img[:, :, 0]
    blue_bg = bg[:, :, 0]
    difference = blue_img - blue_bg
    return blue_img, blue_bg, difference


def find_edges_cv(image_cv, a, b):
    edges = cv.Canny(image_cv, a, b)
    return edges


def reduce_noise(image_cv, lowT, highT):
    return np.where((image_cv > lowT) & (image_cv < highT), image_cv, 0)