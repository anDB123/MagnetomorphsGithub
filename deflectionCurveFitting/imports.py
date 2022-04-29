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

from makeDifferenceImage import *
from makeCurveFromDifferenceImage import *
from modelFunctions import *
from modelTheCurve import *
from findFitParameters import *
from curvedPolymerSample import *
from testNoiseReduction import *
from makeGraphs import *
from physicalModel import *
from physicalModelManyCurves import *
from PhysicalModelManyCurvesOptimized import *

graph_dir = "C:/Users/AndyPC/Desktop/MagnetomorphsGithub/graphs/"
mpl.rcParams["savefig.directory"] = graph_dir
