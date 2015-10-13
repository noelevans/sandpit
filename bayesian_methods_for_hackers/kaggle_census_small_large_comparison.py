from matplotlib import pyplot as plt
import numpy as np


def main():
    data = np.genfromtxt("./data/census_data.csv", skip_header=1, delimiter=",")
    plt.scatter(data[:, 1], data[:, 0], alpha=0.5, c="#7A68A6")
    plt.title("Census mail-back rate vs Population")
    plt.ylabel("Mail-back rate")
    plt.xlabel("population of block-group")
    plt.xlim(-100, 15e3)
    plt.ylim(-5, 105)

    i_min = np.argmin(data[:, 0])
    i_max = np.argmax(data[:, 0])

    plt.scatter([data[i_min, 1], data[i_max, 1]],
        [data[i_min, 0], data[i_max, 0]],
        s=60, marker="o", facecolors="none",
        edgecolors="#A60628", linewidths=1.5,
        label="most extreme points")

    plt.legend(scatterpoints=1)
    plt.show()


if __name__ == '__main__':
    main()
