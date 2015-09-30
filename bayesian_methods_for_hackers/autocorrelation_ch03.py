from matplotlib import pyplot as plt
import numpy as np
import pymc as pm


def autocorr(x):
    result = np.correlate(x, x, mode='full')
    result = result / np.max(result)
    return result[result.size / 2:]


def main():
    x_t = pm.rnormal(0, 1, 200)
    x_t[0] = 0
    y_t = np.zeros(200)
    for i in range(1, 200):
        y_t[i] = pm.rnormal(y_t[i - 1], 1)

    plt.plot(y_t, label="$y_t$", lw=3)
    plt.plot(x_t, label="$x_t$", lw=3)
    plt.xlabel("time, $t$")
    plt.legend()
    plt.show()

    colors = ["#348ABD", "#A60628", "#7A68A6"]

    x = np.arange(1, 200)
    plt.bar(x, autocorr(y_t)[1:], width=1, label="$y_t$",
            edgecolor=colors[0], color=colors[0])
    plt.bar(x, autocorr(x_t)[1:], width=1, label="$x_t$",
            color=colors[1], edgecolor=colors[1])

    plt.legend(title="Autocorrelation")
    plt.ylabel("measured correlation \nbetween $y_t$ and $y_{t-k}$.")
    plt.xlabel("k (lag)")
    plt.title("Autocorrelation plot of $y_t$ and $x_t$ for differing $k$ lags.")
    plt.show()


if __name__ == '__main__':
    main()
