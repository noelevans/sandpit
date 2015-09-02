import json
import matplotlib
import numpy as np
import pymc as pm
from matplotlib import pyplot as plt


def main():
    matplotlibrc_path = '/home/noel/repo/playground/matplotlibrc.json'
    matplotlib.rcParams.update(json.load(open(matplotlibrc_path)))

    tau = pm.rdiscrete_uniform(0, 80)
    print tau

    alpha = 1. / 20.
    lambda_1, lambda_2 = pm.rexponential(alpha, 2)
    print lambda_1, lambda_2

    data = np.r_[pm.rpoisson(lambda_1, tau), pm.rpoisson(lambda_2, 80 - tau)]

    def plot_artificial_sms_dataset():
        tau = pm.rdiscrete_uniform(0, 80)
        alpha = 1. / 20.
        lambda_1, lambda_2 = pm.rexponential(alpha, 2)
        data = np.r_[pm.rpoisson(lambda_1, tau), pm.rpoisson(lambda_2, 80 - tau)]
        plt.bar(np.arange(80), data, color="#348ABD")
        plt.bar(tau - 1, data[tau - 1], color="r", label="user behaviour changed")
        plt.xlim(0, 80)

    plt.title("More example of artificial datasets")
    for i in range(1, 5):
        plt.subplot(4, 1, i)
        plot_artificial_sms_dataset()
    plt.show()


if __name__ == '__main__':
    main()
