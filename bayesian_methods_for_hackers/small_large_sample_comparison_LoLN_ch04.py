from matplotlib import pyplot as plt
import numpy as np
import pymc as pm


def main():
    std_height = 15
    mean_height = 150

    n_counties = 5000
    pop_generator = pm.rdiscrete_uniform
    norm = pm.rnormal

    # generate some artificial population numbers
    population = pop_generator(100, 1500, size=n_counties)

    average_across_county = np.zeros(n_counties)
    for i in range(n_counties):
        # generate some individuals and take the mean
        average_across_county[i] = norm(mean_height, 1. / std_height ** 2,
                                        size=population[i]).mean()

    # located the counties with the apparently most extreme average heights.
    i_min = np.argmin(average_across_county)
    i_max = np.argmax(average_across_county)

    # plot population size vs. recorded average
    plt.scatter(population, average_across_county, alpha=0.5, c="#7A68A6")
    plt.scatter([population[i_min], population[i_max]],
                [average_across_county[i_min], average_across_county[i_max]],
                s=60, marker="o", facecolors="none",
                edgecolors="#A60628", linewidths=1.5,
                label="extreme heights")

    plt.xlim(100, 1500)
    plt.title("Average height vs. County Population")
    plt.xlabel("County Population")
    plt.ylabel("Average height in county")
    plt.plot([100, 1500], [150, 150], color="k", label="true expected \
    height", ls="--")
    plt.legend(scatterpoints=1)
    plt.show()


if __name__ == '__main__':
    main()
