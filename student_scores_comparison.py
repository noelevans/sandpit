from matplotlib import pyplot as plt
import numpy as np


""" Implementing a slide from a PyCon talk, Statistics for Hackers.

    https://speakerdeck.com/pycon2016/jake-vanderplas-statistics-for-hackers
    The question posed:
    "Student_1 gets
        84, 72, 57, 46, 63, 76, 99, 91.                 Mean: 73.5
     Student_2 gets
        81, 69, 74, 61, 56, 87, 69, 65, 66, 44, 62, 69. Mean: 66.9

    But is the difference in means (6.58) statistically significant?"

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
