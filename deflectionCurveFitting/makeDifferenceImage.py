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


def useOriginalImageForFilter(image_name, background_name, crop_array):
    crop_top, crop_bottom, crop_left, crop_right = crop_array

    img = cv.imread(image_name)

    img = img[crop_top:crop_bottom, crop_left:crop_right]

    return img


def blue_only_reduce_noise(image_cv, lowT, highT):
    return np.where((image_cv > lowT) & (image_cv < highT), image_cv, 0)


def any_hsv_reduce_noise(image_cv, hsv_noise_reduction_array):
    hsv_img = cv.cvtColor(image_cv, cv.COLOR_BGR2HSV)
    lowH, highH = hsv_noise_reduction_array[0]
    lowS, highS = hsv_noise_reduction_array[1]
    lowV, highV = hsv_noise_reduction_array[2]
    mask = cv.inRange(hsv_img, (lowH, lowS, lowV), (highH, highS, highV))
    filtered_image = cv.bitwise_and(image_cv, image_cv, mask=mask)
    filtered_hsv = cv.bitwise_and(hsv_img, hsv_img, mask=mask)
    blue_channel = filtered_image[:, :, 0]
    hue_channel = filtered_hsv[:, :, 0]
    grayscale = cv.cvtColor(filtered_image, cv.COLOR_BGR2GRAY)
    final_image = grayscale
    print("Made difference image")
    return final_image


def any_colour_reduce_noise(image_cv, rgb_noise_reduction_array):
    lowR, highR = rgb_noise_reduction_array[0]
    lowG, highG = rgb_noise_reduction_array[1]
    lowB, highB = rgb_noise_reduction_array[2]
    mask = cv.inRange(image_cv, (lowB, lowG, lowR), (highB, highG, highR))
    filtered_image = cv.bitwise_and(image_cv, image_cv, mask=mask)
    blue_channel = filtered_image[:, :, 0]
    grayscale = cv.cvtColor(filtered_image, cv.COLOR_BGR2GRAY)
    final_image = grayscale
    print("Made difference image")
    return blue_channel


def make_hsv_comparison_grid(initial_difference_image, rows, columns, limits_array, number_choice,
                             any_colour_noise_reduction_array):
    fig, axs = plt.subplots(rows, columns)
    hue_min_vals = np.linspace(limits_array[0], limits_array[1], rows)
    hue_max_vals = np.linspace(limits_array[2], limits_array[3], columns)
    for i in range(rows):
        for j in range(columns):
            any_colour_noise_reduction_array[number_choice] = [hue_min_vals[i], hue_max_vals[j]]
            initial_difference_image.changeHSVNoiseReduction(any_colour_noise_reduction_array)
            initial_difference_image.show_difference_image(axs[i, j])
            axs[i, j].set_title(
                "Limit = {}, {}".format(any_colour_noise_reduction_array[number_choice][0],
                                        any_colour_noise_reduction_array[number_choice][1]))
    plt.show()
