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

STUDENT_1 = [84, 72, 57, 46, 63, 76, 99, 91]
STUDENT_2 = [81, 69, 74, 61, 56, 87, 69, 65, 66, 44, 62, 69]


def trial():
    scores = np.array(STUDENT_1 + STUDENT_2)
    np.random.shuffle(scores)
    score_1, score_2 = scores[:len(STUDENT_1)], scores[len(STUDENT_1):]
    return score_1.mean() - score_2.mean()


def main():
    scores = []
    tests = 100000
    for _ in range(tests):
        scores.append(trial())

    plt.hist(scores, 20)
    plt.show()

if __name__ == '__main__':
    main()
