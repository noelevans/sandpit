from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import beta
import seaborn as sns


def main():
    a =  81
    b = 219
    stats = beta.stats(a, b, moments='mvsk')
    print('Mean: %.3f, Variance: %.3f, Skew: %.3f, Kurtosis: %.3f' % stats)
    x = np.linspace(0, 1, 1000)
    y = beta.pdf(x, a, b)
    plt.plot(x, y, 'r-', lw=2, alpha=0.6, label='beta pdf')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
