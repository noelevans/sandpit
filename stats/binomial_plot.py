import numpy as np
import random
import matplotlib.pylab as plt

from collections import Counter


def run_trial():
    coin_tosses = 10
    p = 0.5
    successes = 0
    for t in range(coin_tosses):
        if random.random() < p:
            successes = successes + 1
    return successes


def main():
    trials = 100000
    counts = [run_trial() for n in range(trials)]
    counts = [run_trial() for n in range(trials)]
    print Counter(counts)
    plt.figure()
    _, _, _ = plt.hist(counts, range(12), normed=1, align='left', fill=True)
    plt.xlim([-0.5, 10.5])
    plt.show()

    # Equivalent way to generate binomial distribution using numpy
    n, p = 10, .5 # number of trials, probability of each trial
    counts = np.random.binomial(n, p, 100000)


if __name__ == '__main__':
    main()
