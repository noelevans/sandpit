import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt


def main():
    x = np.linspace(-8, 7, 150)
    mu = (-2, 0, 3)
    tau = (.7, 1, 2.8)
    colors = ["#348ABD", "#A60628", "#7A68A6"]
    parameters = zip(mu, tau, colors)

    for _mu, _tau, _color in parameters:
        plt.plot(x, stats.norm.pdf(x, _mu, scale=1. / _tau),
                 label="$\mu = %d,\;\\tau = %.1f$" % (_mu, _tau), color=_color)
        plt.fill_between(x, stats.norm.pdf(x, _mu, scale=1. / _tau),
                         color=_color, alpha=.33)

    plt.legend(loc="upper right")
    plt.xlabel("$x$")
    plt.ylabel("density function at $x$")
    plt.title("Probability distribution of three different Normal random \
    variables")
    plt.show()


if __name__ == '__main__':
    main()
