from matplotlib import pyplot as plt
import numpy as np
import pymc as pm
from scipy.stats.mstats import mquantiles

from IPython.core.pylabtools import figsize


def logistic(x, beta, alpha=0):
    return 1.0 / (1.0 + np.exp(np.dot(beta, x) + alpha))


def main():
    np.set_printoptions(precision=3, suppress=True)
    challenger_data = np.genfromtxt("challenger_data.csv", skip_header=1,
                                    usecols=[1, 2], missing_values="NA",
                                    delimiter=",")
    # drop the NA values
    challenger_data = challenger_data[~np.isnan(challenger_data[:, 1])]

    temperature = challenger_data[:, 0]
    D = challenger_data[:, 1]  # defect or not?

    # notice the "value" here. We explain why below.
    beta = pm.Normal("beta", 0, 0.001, value=0)
    alpha = pm.Normal("alpha", 0, 0.001, value=0)


    @pm.deterministic
    def p(t=temperature, alpha=alpha, beta=beta):
        return 1.0 / (1. + np.exp(beta * t + alpha))

    # connect the probabilities in `p` with our observations through a
    # Bernoulli random variable.
    observed = pm.Bernoulli("bernoulli_obs", p, value=D, observed=True)

    model = pm.Model([observed, beta, alpha])

    # Mysterious code to be explained in Chapter 3
    map_ = pm.MAP(model)
    map_.fit()
    mcmc = pm.MCMC(model)
    mcmc.sample(120000, 100000, 2)


    alpha_samples = mcmc.trace('alpha')[:, None]  # best to make them 1d
    beta_samples = mcmc.trace('beta')[:, None]


    figsize(12.5, 6)

    # histogram of the samples:
    plt.subplot(211)
    plt.title(r"Posterior distributions of the variables $\alpha, \beta$")
    plt.hist(beta_samples, histtype='stepfilled', bins=35, alpha=0.85,
             label=r"posterior of $\beta$", color="#7A68A6", normed=True)
    plt.legend()

    plt.subplot(212)
    plt.hist(alpha_samples, histtype='stepfilled', bins=35, alpha=0.85,
             label=r"posterior of $\alpha$", color="#A60628", normed=True)
    plt.legend()
    plt.show()


    t = np.linspace(temperature.min() - 5, temperature.max() + 5, 50)[:, None]
    p_t = logistic(t.T, beta_samples, alpha_samples)
    mean_prob_t = p_t.mean(axis=0)

    plt.plot(t, mean_prob_t, lw=3, label="average posterior \nprobability \
        of defect")
    plt.plot(t, p_t[0, :], ls="--", label="realization from posterior")
    plt.plot(t, p_t[-2, :], ls="--", label="realization from posterior")
    plt.scatter(temperature, D, color="k", s=50, alpha=0.5)
    plt.title("Posterior expected value of probability of defect; \
        plus realizations")
    plt.legend(loc="lower left")
    plt.ylim(-0.1, 1.1)
    plt.xlim(t.min(), t.max())
    plt.ylabel("probability")
    plt.xlabel("temperature")
    plt.show()


    # vectorized bottom and top 2.5% quantiles for "confidence interval"
    qs = mquantiles(p_t, [0.025, 0.975], axis=0)
    plt.fill_between(t[:, 0], *qs, alpha=0.7,
                     color="#7A68A6")

    plt.plot(t[:, 0], qs[0], label="95% CI", color="#7A68A6", alpha=0.7)

    plt.plot(t, mean_prob_t, lw=1, ls="--", color="k",
             label="average posterior \nprobability of defect")

    plt.xlim(t.min(), t.max())
    plt.ylim(-0.02, 1.02)
    plt.legend(loc="lower left")
    plt.scatter(temperature, D, color="k", s=50, alpha=0.5)
    plt.xlabel("temp, $t$")

    plt.ylabel("probability estimate")
    plt.title("Posterior probability estimates given temp. $t$")
    plt.show()


    prob_31 = logistic(31, beta_samples, alpha_samples)

    plt.xlim(0.995, 1)
    plt.hist(prob_31, bins=1000, normed=True, histtype='stepfilled')
    plt.title("Posterior distribution of probability of defect, given $t = 31$")
    plt.xlabel("probability of defect occurring in O-ring")
    plt.show()


    simulated = pm.Bernoulli("bernoulli_sim", p)
    N = 10000

    mcmc = pm.MCMC([simulated, alpha, beta, observed])
    mcmc.sample(N)

    simulations = mcmc.trace("bernoulli_sim")[:]
    plt.title("Simulated dataset using posterior parameters")
    for i in range(4):
        ax = plt.subplot(4, 1, i + 1)
        plt.scatter(temperature, simulations[1000 * i, :], color="k",
                    s=50, alpha=0.6)
    plt.show()


    # Chapter 2, question 2
    # The plot shows negative correlation because you get the same
    # intersection with the danger / safe divide temperature. Up the beta
    # value and alpha must fall to have the correct dependent distinction
    plt.scatter(alpha_samples, beta_samples, alpha=0.1)
    plt.title("Why does the plot look like this?")
    plt.xlabel(r"$\alpha$")
    plt.ylabel(r"$\beta$")


if __name__ == '__main__':
    main()
