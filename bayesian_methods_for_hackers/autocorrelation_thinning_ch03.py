from matplotlib import pyplot as plt
import numpy as np
import pymc as pm


def autocorr(x):
    result = np.correlate(x, x, mode='full')
    result = result / np.max(result)
    return result[result.size / 2:]


def main():
    """ Demonstrating thinning of two autocorrelated inputs (representing
        posterior probabilities). The key point is the thinned - every 2nd / 3rd
        point - functions approach zero quicker. More thinning is better (but
        expensive)
    """

    # x_t = pm.rnormal(0, 1, 200)
    # x_t[0] = 0
    y_t = np.zeros(200)
    for i in range(1, 200):
        y_t[i] = pm.rnormal(y_t[i - 1], 1)

    max_x = 200 / 3 + 1
    x = np.arange(1, max_x)

    colors = ["#348ABD", "#A60628", "#7A68A6"]
    plt.bar(x, autocorr(y_t)[1:max_x], edgecolor=colors[0],
            label="no thinning", color=colors[0], width=1)
    plt.bar(x, autocorr(y_t[::2])[1:max_x], edgecolor=colors[1],
            label="keeping every 2nd sample", color=colors[1], width=1)
    plt.bar(x, autocorr(y_t[::3])[1:max_x], width=1, edgecolor=colors[2],
            label="keeping every 3rd sample", color=colors[2])

    plt.autoscale(tight=True)
    plt.legend(title="Autocorrelation plot for $y_t$", loc="lower left")
    plt.ylabel("measured correlation \nbetween $y_t$ and $y_{t-k}$.")
    plt.xlabel("k (lag)")
    plt.title("Autocorrelation of $y_t$ (no thinning vs. thinning) \
            at differing $k$ lags.")
    plt.show()


if __name__ == '__main__':
    main()
