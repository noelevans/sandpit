import pymc as pm
from matplotlib import pyplot as plt


def main():
    # The parameters are the bounds of the Uniform.
    p = pm.Uniform('p', lower=0, upper=1)

    # set constants
    p_true = 0.05  # remember, this is unknown.
    N = 1500

    # sample N Bernoulli random variables from Ber(0.05).
    # each random variable has a 0.05 chance of being a 1.
    # this is the data-generation step
    occurrences = pm.rbernoulli(p_true, N)

    print occurrences
    print occurrences.sum()

    # Occurrences.mean is equal to n/N.
    print "What is the observed frequency in Group A? %.4f" % occurrences.mean()
    print "Does this equal the true frequency? %s" % (occurrences.mean() == p_true)

    # include the observations, which are Bernoulli
    obs = pm.Bernoulli("obs", p, value=occurrences, observed=True)

    # To be explained in chapter 3
    mcmc = pm.MCMC([p, obs])
    mcmc.sample(18000, 1000)

    plt.title("Posterior distribution of $p_A$, the true effectiveness of site A")
    plt.vlines(p_true, 0, 90, linestyle="--", label="true $p_A$ (unknown)")
    plt.hist(mcmc.trace("p")[:], bins=25, histtype="stepfilled", normed=True)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()