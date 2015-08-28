import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


def main():
    a = np.linspace(0, 4, 100)
    lambda_ = [0.5, 1]
    colours = ["#348ABD", "#A60628"]

    for l, c in zip(lambda_, colours):
        plt.plot(a, stats.expon.pdf(a, scale=1. / l), lw=3,
                 color=c, label="$\lambda = %.1f$" % l)
        plt.fill_between(a, stats.expon.pdf(a, scale=1. / l), color=c, alpha=.3)

    plt.legend()
    plt.ylabel("PDF at $z$")
    plt.xlabel("$z$")
    plt.ylim(0, 1.2)
    plt.title("Probability density function of an Exponential random variable;\
     differing $\lambda$");
    plt.show()


if __name__ == '__main__':
    main()
