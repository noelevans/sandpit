import numpy as np
import matplotlib.pyplot as plt
import pymc as pm


def main():
    N_Y = 250  # use this many to approximate D(N)
    # use this many samples in the approx. to the variance.
    N_array = np.arange(1000, 50000, 2500)
    D_N_results = np.zeros(len(N_array))

    lambda_ = 4.5
    expected_value = lambda_  # for X ~ Poi(lambda) , E[ X ] = lambda

    def D_N(n):
        """
        This function approx. D_n, the average variance of using n samples.
        """
        Z = pm.rpoisson(lambda_, size=(n, N_Y))
        average_Z = Z.mean(axis=0)
        return np.sqrt(((average_Z - expected_value) ** 2).mean())


    for i, n in enumerate(N_array):
        D_N_results[i] = D_N(n)


    plt.xlabel("$N$")
    plt.ylabel("expected squared-distance from true value")
    plt.plot(N_array, D_N_results, lw=3,
             label="expected distance between\n\
    expected value and \naverage of $N$ random variables.")
    plt.plot(N_array, np.sqrt(expected_value) / np.sqrt(N_array), lw=2, ls="--",
             label=r"$\frac{\sqrt{\lambda}}{\sqrt{N}}$")
    plt.legend()
    plt.title("How 'fast' is the sample average converging? ")
    plt.show()


if __name__ == '__main__':
    main()
