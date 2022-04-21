from imports import *

def makeDifferenceImage(image_name, background_name, crop_array):
    crop_top, crop_bottom, crop_left, crop_right = crop_array

    img = cv.imread(image_name)

    bg = cv.imread(background_name)

    img = img[crop_top:crop_bottom, crop_left:crop_right]
    bg = bg[crop_top:crop_bottom, crop_left:crop_right]
    blue_img = img[:, :, 0]
    blue_bg = bg[:, :, 0]
    difference = blue_img - blue_bg
    return difference

def reduce_noise(image_cv, lowT, highT):
    return np.where((image_cv > lowT) & (image_cv < highT), image_cv, 0)




