from imports import *


def makeBlueOnlyDifferenceImage(image_name, background_name, crop_array):
    crop_top, crop_bottom, crop_left, crop_right = crop_array

    img = cv.imread(image_name)

    bg = cv.imread(background_name)

    img = img[crop_top:crop_bottom, crop_left:crop_right]
    bg = bg[crop_top:crop_bottom, crop_left:crop_right]
    blue_img = img[:, :, 0]
    blue_bg = bg[:, :, 0]
    difference = blue_img - blue_bg
    return difference


def makeAnyColourDifferenceImage(image_name, background_name, crop_array):
    crop_top, crop_bottom, crop_left, crop_right = crop_array

    img = cv.imread(image_name)

    bg = cv.imread(background_name)

    img = img[crop_top:crop_bottom, crop_left:crop_right]
    bg = bg[crop_top:crop_bottom, crop_left:crop_right]
    difference = img - bg
    return difference


def blue_only_reduce_noise(image_cv, lowT, highT):
    return np.where((image_cv > lowT) & (image_cv < highT), image_cv, 0)


def any_colour_reduce_noise(image_cv, lowH, highH, lowS, highS, lowV, highV):
    hsv_img = cv.cvtColor(image_cv, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv_img, (lowH, lowS, lowV), (highH, highS, highV))
    filtered_image = cv.bitwise_and(image_cv, image_cv, mask=mask)
    filteered_hsv = cv.bitwise_and(hsv_img, hsv_img, mask=mask)
    final_image = filtered_image[:, :, 0]
    print("Made difference image")
    return final_image
