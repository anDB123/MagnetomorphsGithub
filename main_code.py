from imports import *
testNoiseReduction=True
testCropping=True
bg_29= "29redBackground/DSC_0068 (3).JPG"
im_array_29 = [
    "29redBackground/DSC_0067 (3).JPG",
    "29redBackground/DSC_0079 (3).JPG",
    "29redBackground/DSC_0090 (3).JPG",
    "29redBackground/DSC_0096 (3).JPG",
               ]
crop_29 = [130,1200,300,2700]
#makeDifferenceImage
diff_im = makeDifferenceImage(image_name=im_array_29[0], background_name=bg_29, crop_array=crop_29)
diff_im = reduce_noise(diff_im,100,170)
plt.imshow(diff_im)
#makeCurveFromDifferenceImage
x_data, y_data = makeCurveFromDifferenceImage(diff_im)
plt.scatter(x_data,y_data)
#modelTheCurve

#makePlots
#displayPlots
plt.show()