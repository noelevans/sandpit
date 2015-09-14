from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import scipy.stats as stats

from IPython.core.pylabtools import figsize


def main():
    figsize(12.5, 5)
    fig = plt.figure()
    jet = plt.cm.jet
    plt.subplot(121)

    x = y = np.linspace(0, 5, 100)
    X, Y = np.meshgrid(x, y)

    exp_x = stats.expon.pdf(x, scale=3)
    exp_y = stats.expon.pdf(x, scale=10)
    M = np.dot(exp_x[:, None], exp_y[None, :])
    CS = plt.contour(X, Y, M)
    im = plt.imshow(M, interpolation='none', origin='lower',
                    cmap=jet, extent=(0, 5, 0, 5))
    plt.xlabel("prior on $p_1$")
    plt.ylabel("prior on $p_2$")
    plt.title("$Exp(3), Exp(10)$ prior landscape")

    ax = fig.add_subplot(122, projection='3d')
    ax.plot_surface(X, Y, M, cmap=jet)
    ax.view_init(azim=390)
    plt.title("$Exp(3), Exp(10)$ prior landscape; \nalternate view")
    plt.show()

if __name__ == '__main__':
    main()
