import numpy as np
import cv2 as cv
import matplotlib as mpl
import os
from matplotlib import pyplot as plt
import matplotlib.pylab as pl
import math
from scipy.optimize import curve_fit
import scipy.stats
import copy
import time
import re

from deflectionCurveFitting.makeDifferenceImage import *
from deflectionCurveFitting.makeCurveFromDifferenceImage import *
from deflectionCurveFitting.modelFunctions import *
from deflectionCurveFitting.modelTheCurve import *
from deflectionCurveFitting.findFitParameters import *
from deflectionCurveFitting.curvedPolymerSample import *
from deflectionCurveFitting.testNoiseReduction import *
# from deflectionCurveFitting.makeGraphs import *
from deflectionCurveFitting.physicalModel import *
from deflectionCurveFitting.physicalModelManyCurves import *
from deflectionCurveFitting.PhysicalModelManyCurvesOptimized import *
from deflectionCurveFitting.PhysicalModelManyCurvesGradient import *

graph_dir = "C:/Users/AndyPC/Desktop/MagnetomorphsGithub/graphs/"
mpl.rcParams["savefig.directory"] = graph_dir
