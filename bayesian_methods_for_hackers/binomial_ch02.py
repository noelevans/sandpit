from matplotlib import pyplot as plt
import numpy as np
from scipy import stats

from IPython.core.pylabtools import figsize


def main():
    figsize(12.5, 4)
    parameters = [(10, .4), (10, .9)]
    colors = ["#348ABD", "#A60628"]

    for params, cols in zip(parameters, colors):
        N, p = params
        _x = np.arange(N + 1)
        plt.bar(_x - 0.5, stats.binom.pmf(_x, N, p), color=cols,
                edgecolor=cols,
                alpha=0.6,
                label="$N$: %d, $p$: %.1f" % (N, p),
                linewidth=3)

    plt.legend(loc="upper left")
    plt.xlim(0, 10.5)
    plt.xlabel("$k$")
    plt.ylabel("$P(X = k)$")
    plt.title("Probability mass distributions of binomial random variables")
    plt.show()


if __name__ == '__main__':
    main()
