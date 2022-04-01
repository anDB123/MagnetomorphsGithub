import scipy.optimize

from imports import *

def modelTheCurve(x_values, y_values):
    model_name = quadratic_fit
    initGuess = [0,0,0]
    optimisedParams, covarianceMatrix = scipy.optimize.curve_fit(model_name, x_values, y_values, p0=initGuess)
    return x_values, model_name(x_values,*optimisedParams)