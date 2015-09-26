from matplotlib import pyplot as plt
import numpy as np


""" Demonstrate Law of Large numbers

Example of the Law of Large numbers showing a 50-50 (say a coin toss) converging
to 0.5 average with time. For practice, the code uses numpy to build a
triangule of 1s in a 2d matrix so each row represents a further addition of new
data. The iterated version is given underneath for comparison

"""

def main():
    N = 10000     # this runs very hard on memory
    rs = np.random.randint(0, 1+1, N)
    tri = np.tri(N)
    ys = (rs * tri).sum(1) / tri.sum(1)
    plt.plot(np.arange(N), ys)
    plt.show()

    # Much easier (and lighter on memory) in std python
    ys = []
    for n in range(1, N+1):
        ys.append(rs[:n].mean())
    plt.plot(np.arange(N), ys)
    plt.show()


if __name__ == '__main__':
    main()
