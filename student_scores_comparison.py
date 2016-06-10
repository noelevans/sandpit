from matplotlib import pyplot as plt
import numpy as np


""" Implementing a slide from a PyCon talk, Statistics for Hackers.

    https://speakerdeck.com/pycon2016/jake-vanderplas-statistics-for-hackers
    The question posed:
    "Two students get the following scores over a term's modules:

    student_1 84, 72, 57, 46, 63, 76, 99, 91:                 mean 73.5
    student_2 81, 69, 74, 61, 56, 87, 69, 65, 66, 44, 62, 69: mean 66.9

    Student_1 has an average of 6.6% more than student_2.
    Is this difference statistically significant?

"""

SCORES_1 = np.array([84, 72, 57, 46, 63, 76, 99, 91,
                     81, 69, 74, 61, 56, 87, 69, 65, 66, 44, 62, 69])
SCORES_2 = np.array([73, 73, 73, 73, 73, 74, 74, 74,
                     67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 66])

def trial(scores):
    np.random.shuffle(scores)
    student_1 = scores[:8]
    student_2 = scores[8:]
    return student_1.mean() - student_2.mean()


def main():
    tests = 1000000
    scores_1 = [trial(SCORES_1) for _ in range(tests)]
    scores_2 = [trial(SCORES_2) for _ in range(tests)]

    plt.hist(scores_1, 16, color='blue', alpha=0.4)
    plt.hist(scores_2, 16, color='red', alpha=0.3)
    plt.show()


if __name__ == '__main__':
    main()
