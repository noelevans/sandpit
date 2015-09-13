from matplotlib import pyplot as plt
import numpy as np
import scipy.stats as stats

from IPython.core.pylabtools import figsize
from mpl_toolkits.mplot3d import Axes3D


def main():
    figsize(12.5, 4)

    jet = plt.cm.jet
    fig = plt.figure()
    x = y = np.linspace(0, 5, 100)
    X, Y = np.meshgrid(x, y)

    plt.subplot(121)
    uni_x = stats.uniform.pdf(x, loc=0, scale=5)
    uni_y = stats.uniform.pdf(y, loc=0, scale=5)
    M = np.dot(uni_x[:, None], uni_y[None, :])
    im = plt.imshow(M, interpolation='none', origin='lower',
                    cmap=jet, vmax=1, vmin=-.15, extent=(0, 5, 0, 5))

    plt.xlim(0, 5)
    plt.ylim(0, 5)
    plt.title("Landscape formed by Uniform priors.")

    ax = fig.add_subplot(122, projection='3d')
    ax.plot_surface(X, Y, M, cmap=plt.cm.jet, vmax=1, vmin=-.15)
    ax.view_init(azim=390)
    plt.title("Uniform prior landscape; alternate view")
    plt.show()


if __name__ == '__main__':
    main()
