import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import numpy as np

fig = plt.figure(figsize=(8, 8))

gs = fig.add_gridspec(2,2)

x=np.linspace(0,2*np.pi,100)
y1=np.sin(x)
y2=np.cos(x)
y3=np.tan(x)
fig.add_subplot(gs[0, 0]).plot(x,y1)
fig.add_subplot(gs[0, 1]).plot(x,y2)
fig.add_subplot(gs[1, 0]).plot(x,y3)


plt.show()