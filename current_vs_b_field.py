import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import MaxNLocator
import numpy as np
import matplotlib.patches as patches

current_array = [0,0.502,1.003,1.51,2.026,2.506,2.999,3.484,3.969]
magnetic_field_array=[0.05,0.38,0.82,1.25,1.7,2.12,2.54,2.96,3.38]
plt.plot(current_array,magnetic_field_array)
plt.xlabel("Current (A)")
plt.ylabel("Magnetic Field Strength (mT)")
plt.show()