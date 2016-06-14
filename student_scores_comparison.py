from matplotlib import pyplot as plt
import numpy as np
import unittest


""" Implementing a slide from a PyCon talk, Statistics for Hackers.

    https://speakerdeck.com/pycon2016/jake-vanderplas-statistics-for-hackers
    The question posed:
    "Two students get the following scores over a term's modules:

    student_1 84, 72, 57, 46, 63, 76, 99, 91:                 mean 73.5
    student_2 81, 69, 74, 61, 56, 87, 69, 65, 66, 44, 62, 69: mean 66.9

    Student_1 has an average of 6.6% more than student_2.
    Is this difference statistically significant?

"""

STUDENT_1 = [84, 72, 57, 46, 63, 76, 99, 91]
STUDENT_2 = [81, 69, 74, 61, 56, 87, 69, 65, 66, 44, 62, 69]
STUDENT_3 = [73, 73, 73, 73, 73, 74, 74, 74]
STUDENT_4 = [67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 66]

SCORES_1 = np.array(STUDENT_1 + STUDENT_2)
SCORES_2 = np.array(STUDENT_3 + STUDENT_4)

def trial(scores):
    np.random.shuffle(scores)
    student_1 = scores[:8]
    student_2 = scores[8:]
    return student_1.mean() - student_2.mean()


def significance_bound(hist, x):
    freq, widths, _ = hist
    normed_freq = freq.cumsum() / freq.sum()
    midpoints = (widths[:-1] + widths[1:]) / 2
    return np.interp(x, normed_freq, midpoints)


def main():
    tests = 100000
    net_scores_1 = [trial(SCORES_1) for _ in range(tests)]
    net_scores_2 = [trial(SCORES_2) for _ in range(tests)]

    h1 = plt.hist(net_scores_1, 16, color='darkblue', alpha=0.4,
                  label=r'$scoring_1$')
    h2 = plt.hist(net_scores_2, 16, color='red', alpha=0.7,
                  label=r'$scoring_2$')

    actual_difference = 73.5 - 66.9
    plt.axvline(actual_difference, lw=2, color='black',
                label=r'$Actual\ score\ difference$')
    plt.axvspan(significance_bound(h1, 0.05),
                significance_bound(h1, 0.95),
                color='skyblue',
                alpha=0.3,
                label=r'$2\sigma_1$')
    plt.axvspan(significance_bound(h2, 0.05),
                significance_bound(h2, 0.95),
                color='salmon',
                alpha=0.4,
                label=r'$2\sigma_2$')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
