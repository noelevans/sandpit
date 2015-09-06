from matplotlib import pyplot as plt
import numpy as np
import pymc as pm

from IPython.core.pylabtools import figsize


def main():
    figsize(12.5, 3.5)
    np.set_printoptions(precision=3, suppress=True)
    challenger_data = np.genfromtxt("challenger_data.csv", skip_header=1,
                                    usecols=[1, 2], missing_values="NA",
                                    delimiter=",")
    # drop the NA values
    challenger_data = challenger_data[~np.isnan(challenger_data[:, 1])]

    # plot it, as a function of temperature (the first column)
    print "Temp (F), O-Ring failure?"
    print challenger_data

    plt.scatter(challenger_data[:, 0], challenger_data[:, 1], s=75, color="k",
                alpha=0.5)
    plt.yticks([0, 1])
    plt.ylabel("Damage Incident?")
    plt.xlabel("Outside temperature (Fahrenheit)")
    plt.title("Defects of the Space Shuttle O-Rings vs temperature")
    plt.show()


if __name__ == '__main__':
    main()
