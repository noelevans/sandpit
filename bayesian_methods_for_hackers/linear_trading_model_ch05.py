from matplotlib import pyplot as plt
import numpy as np
import pymc as pm
from pymc.Matplot import plot as mcplot


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

    std = pm.Uniform("std", 0, 100, trace=False)

    @pm.deterministic
    def prec(U=std):
        return 1.0 / (U) ** 2

    beta = pm.Normal("beta", 0, 0.0001)
    alpha = pm.Normal("alpha", 0, 0.0001)


    @pm.deterministic
    def mean(X=X, alpha=alpha, beta=beta):
        return alpha + beta * X

    obs = pm.Normal("obs", mean, prec, value=Y, observed=True)
    mcmc = pm.MCMC([obs, beta, alpha, std, prec])

    mcmc.sample(100000, 80000)
    mcplot(mcmc)


if __name__ == '__main__':
    main()
