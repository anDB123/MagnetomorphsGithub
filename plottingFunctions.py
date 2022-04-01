from matplotlib import pyplot as plt


def plot_image(ax, img):
    ax.imshow(img, cmap='gray')


def ax_plot_scatter(ax, x_values, y_values, label):
    ax.scatter(x_values, y_values, s=2, label=label)


def plot_triple_fit(ax, x_model_array, y_model_array, a, b):
    plt.axvline(x=a, label="Start {:.1f}".format(a),color='r')
    plt.axvline(x=b, label="End {:.1f}".format(b),color='r')
    ax.plot(x_model_array, y_model_array,color='r',linewidth = 1)


def plot_image_with_fit(ax, image, x_edges, y_edges, x_model_array, y_model_array, chi_squared_label, a, b):
    plt.xticks([])
    plt.yticks([])
    plt.title(chi_squared_label)
    plot_image(ax, image)
    ax_plot_scatter(ax, x_edges, y_edges, label="Edges")
    plot_triple_fit(ax, x_model_array, y_model_array, a, b)
