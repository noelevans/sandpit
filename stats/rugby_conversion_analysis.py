from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import beta
import seaborn as sns


def mean(a, b):
    """ Statistical mean of distributon defined by alpha and beta values. """
    return a / float(a + b)


def main():
    """ Two beta distributions with the same mean but differing variance.

    The distributions reflect kicking averages of a player who has been very
    consistent through his career verses another who has had a range of better
    and worse years. On the x-axis, we see the expected score ratio over the
    season - the y-axis indicating the likelihood of that average

    The prime graphs (lighter colouring) show the change in belief for the
    players' expected season average after 4 kicks (trials) where only 1 was
    successful. The more consistent player's season expectation changes very
    little relative to the more varied player.

    Adapted from this explanation:
    http://varianceexplained.org/statistics/beta_distribution_and_baseball/

    """
    a_1 = 61
    b_1 = 20
    a_2 = 610
    b_2 = 200

    this_season_scores = 1
    this_season_misses = 3

    print(mean(a_1, b_1))
    print(mean(a_2, b_2))

    x = np.linspace(0, 1, 1000)
    y_1 = beta.pdf(x, a_1, b_1)
    y_2 = beta.pdf(x, a_2, b_2)
    y_1_prime = beta.pdf(x, a_1 + this_season_scores, b_1 + this_season_misses)
    y_2_prime = beta.pdf(x, a_2 + this_season_scores, b_2 + this_season_misses)

    plt.plot(x, y_1,       'r', lw=2, alpha=0.8, label='a =  61, b =  20')
    plt.plot(x, y_1_prime, 'r', lw=2, alpha=0.2, label='a =  62, b =  23')
    plt.plot(x, y_2,       'b', lw=2, alpha=0.8, label='a = 610, b = 200')
    plt.plot(x, y_2_prime, 'b', lw=2, alpha=0.2, label='a = 611, b = 203')

    plt.xlim(0.3, 1.0)
    plt.xlabel('p(scoring)')
    plt.ylabel('probability density')
    plt.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    main()
