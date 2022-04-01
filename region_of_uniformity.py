import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import MaxNLocator
import numpy as np
import matplotlib.patches as patches

z1 = [
    [8.12, 6.26, 5.13, 4.24, 4.3],
    [7.53, 6.45, 5.73, 5.22, 5.07],
    [7, 6.53, 6.01, 5.66, 5.57],
    [6.59, 6.38, 6.12, 5.91, 5.97],
    [6.32, 6.26, 6.1, 6.01, 5.98],
    [6.15, 6.17, 6.09, 6.05, 6.04],
    [6.06, 6.09, 6.06, 6.05, 6.08],
    [6, 6.02, 6.05, 6.05, 6.02],
    [5.91, 6.02, 6.05, 6.06, 6.07],
    [6.01, 6.03, 6.03, 6.05, 6.04]]
z2 = [
    [8.12, 6.26, 5.13, 4.24, 4.3, 4.24, 5.13, 6.26, 8.12],
    [7.53, 6.45, 5.73, 5.22, 5.07, 5.22, 5.73, 6.45, 7.53],
    [7, 6.53, 6.01, 5.66, 5.57, 5.66, 6.01, 6.53, 7],
    [6.59, 6.38, 6.12, 5.91, 5.97, 5.91, 6.12, 6.38, 6.59],
    [6.32, 6.26, 6.1, 6.01, 5.98, 6.01, 6.1, 6.26, 6.32],
    [6.15, 6.17, 6.09, 6.05, 6.04, 6.05, 6.09, 6.17, 6.15],
    [6.06, 6.09, 6.06, 6.05, 6.08, 6.05, 6.06, 6.09, 6.06],
    [6, 6.02, 6.05, 6.05, 6.02, 6.05, 6.05, 6.02, 6],
    [5.91, 6.02, 6.05, 6.06, 6.07, 6.06, 6.05, 6.02, 5.91],
    [6, 6.02, 6.05, 6.05, 6.02, 6.05, 6.05, 6.02, 6],
    [6.06, 6.09, 6.06, 6.05, 6.08, 6.05, 6.06, 6.09, 6.06],
    [6.15, 6.17, 6.09, 6.05, 6.04, 6.05, 6.09, 6.17, 6.15],
    [6.32, 6.26, 6.1, 6.01, 5.98, 6.01, 6.1, 6.26, 6.32],
    [6.59, 6.38, 6.12, 5.91, 5.97, 5.91, 6.12, 6.38, 6.59],
    [7, 6.53, 6.01, 5.66, 5.57, 5.66, 6.01, 6.53, 7],
    [7.53, 6.45, 5.73, 5.22, 5.07, 5.22, 5.73, 6.45, 7.53],
    [8.12, 6.26, 5.13, 4.24, 4.3, 4.24, 5.13, 6.26, 8.12]]


y1, x1 = np.meshgrid(np.linspace(0, 16, 17),
                   np.linspace(0, 8, 9))

y2, x2 = np.meshgrid(np.linspace(0, 16, 17),
                   np.linspace(0, 8, 9))

z = np.transpose(z2)
print(np.shape(x1))
print(np.shape(y1))
print(np.shape(z))
levels = MaxNLocator(nbins=15).tick_values(z.min(), z.max())
cmap = plt.get_cmap('Purples')
norm = colors.LogNorm(vmin=z.min(), vmax=z.max())
norm = colors.CenteredNorm(6.04)



# plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 18


fig, ax = plt.subplots()

im = ax.pcolormesh(x1, y1, z, cmap=cmap, norm=norm)

cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Magnetic Field Strength (mT)', rotation=270,labelpad=30)


fig.tight_layout()
#print(levels)

rect = patches.Rectangle((2, 5), 4, 6, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)

ax.text(4,8,"Uniform Region\n\n(4cm by 6cm)",ha="center",va="center",color='r',fontsize=13)


percentage_allowed = 0.01
contours = [6.04 * (1 - percentage_allowed), 6.04 * (1 + percentage_allowed)]

#cf1 = ax.contourf(x, y, z, cmap=cmap, levels=levels)
cf2 = ax.contour(x2, y2, z, cmap=cmap, levels=contours)

ax.axhline(y=8,color='k',dashes=[2,2])
ax.axvline(x=4,color='k',dashes=[2,2])
ax.text(4.1,15,"Lines of Symmetry",color='k',fontsize=13)
ax.set_xlabel("X Distance (cm)")
ax.set_ylabel("Y distance (cm)")
fmt = {}
strs = ["-10%", "+10%"]
for l, s in zip(cf2.levels, strs):
    fmt[l] = s
ax.clabel(cf2, contours, inline=2, fmt=fmt, fontsize=10, )  # ,contour_labels)

plt.show()
