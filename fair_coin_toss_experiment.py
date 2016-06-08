from __future__ import division
import numpy as np


""" Implementing a slide from a PyCon talk, Statistics for Hackers.

    https://speakerdeck.com/pycon2016/jake-vanderplas-statistics-for-hackers
    The question posed:
        "You toss a coin 30 times and see 22 heads. Is it a fair coin"

    The key line of interest is the the if statement. Notice that we count the
    test as an example of the criteria if 22 heads *or more* are rolled. Not
    just 22 exactly.

"""

def main():
    twenty_twos = 0
    tests = 100000
    for _ in range(tests):
        run = np.random.randint(1+1, size=30)
        if run.sum() >= 22:     # 22
            twenty_twos += 1
    print(twenty_twos / tests)
    print('Reject the null hypothesis; is the coin biased?')
    print('Yes!' if twenty_twos / tests < 0.05 else 'No!')


if __name__ == '__main__':
    main()
