import numpy as np
from matplotlib import pyplot as plt

from IPython.core.pylabtools import figsize


def logistic(x, beta, alpha=0):
    return 1.0 / (1.0 + np.exp(np.dot(beta, x) + alpha))


def main():
    figsize(12, 3)

    x = np.linspace(-4, 4, 100)

    plt.plot(x, logistic(x, 1), label=r"$\beta = 1$", ls="--", lw=1,
             color='#332288')
    plt.plot(x, logistic(x, 3), label=r"$\beta = 3$", ls="--", lw=1,
             color='#117733')
    plt.plot(x, logistic(x, -5), label=r"$\beta = -5$", ls="--", lw=1,
             color='#882255')

    plt.plot(x, logistic(x, 1, 1), label=r"$\beta = 1, \alpha = 1$",
             color="#332288")
    plt.plot(x, logistic(x, 3, -2), label=r"$\beta = 3, \alpha = -2$",
             color="#117733")
    plt.plot(x, logistic(x, -5, 7), label=r"$\beta = -5, \alpha = 7$",
             color="#882255")

    plt.legend(loc="lower left")
    plt.show()


if __name__ == '__main__':
    main()
