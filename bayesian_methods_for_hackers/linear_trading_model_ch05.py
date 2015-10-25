from matplotlib import pyplot as plt
import numpy as np


def main():
    # Code to create artificial data
    N = 100
    X = 0.025 * np.random.randn(N)
    Y = 0.5 * X + 0.01 * np.random.randn(N)

    ls_coef_ = np.cov(X, Y)[0, 1] / np.var(X)
    ls_intercept = Y.mean() - ls_coef_ * X.mean()

    plt.scatter(X, Y, c="k")
    plt.xlabel("trading signal")
    plt.ylabel("returns")
    plt.title("Empirical returns vs trading signal")
    plt.plot(X, ls_coef_ * X + ls_intercept, label="Least-squares line")
    plt.xlim(X.min(), X.max())
    plt.ylim(Y.min(), Y.max())
    plt.legend(loc="upper left")
    plt.show()


if __name__ == '__main__':
    main()
