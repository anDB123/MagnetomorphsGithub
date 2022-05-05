from imports import *
def find_reduced_chi_squared(observed, predicted, errors):
    return np.sum(((observed - predicted) ** 2 / errors) / (np.size(observed) - 1))