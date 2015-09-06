import pymc as pm
from matplotlib import pyplot as plt


def main():
    # these two quantities are unknown to us.
    true_p_A = 0.05
    true_p_B = 0.04

    # notice the unequal sample sizes -- no problem in Bayesian analysis.
    N_A = 1500
    N_B = 750

    # generate some observations
    observations_A = pm.rbernoulli(true_p_A, N_A)
    observations_B = pm.rbernoulli(true_p_B, N_B)

    print observations_A.mean()
    print observations_B.mean()

    # Set up the pymc model. Again assume Uniform priors for p_A and p_B.
    p_A = pm.Uniform("p_A", 0, 1)
    p_B = pm.Uniform("p_B", 0, 1)

    # Define the deterministic delta function. This is our unknown of interest.
    @pm.deterministic
    def delta(p_A=p_A, p_B=p_B):
        return p_A - p_B

    # Set of observations, in this case we have two observation datasets.
    obs_A = pm.Bernoulli("obs_A", p_A, value=observations_A, observed=True)
    obs_B = pm.Bernoulli("obs_B", p_B, value=observations_B, observed=True)

    # To be explained in chapter 3.
    mcmc = pm.MCMC([p_A, p_B, delta, obs_A, obs_B])
    mcmc.sample(20000, 1000)

    p_A_samples = mcmc.trace("p_A")[:]
    p_B_samples = mcmc.trace("p_B")[:]
    delta_samples = mcmc.trace("delta")[:]

    # histogram of posteriors
    ax = plt.subplot(311)
    plt.xlim(0, .1)
    plt.hist(p_A_samples, histtype='stepfilled', bins=25, alpha=0.85,
             label="posterior of $p_A$", color="#A60628", normed=True)
    plt.vlines(true_p_A, 0, 80, linestyle="--", label="true $p_A$ (unknown)")
    plt.legend(loc="upper right")
    plt.title("Posterior distributions of $p_A$, $p_B$, and delta unknowns")

    ax = plt.subplot(312)
    plt.xlim(0, .1)
    plt.hist(p_B_samples, histtype='stepfilled', bins=25, alpha=0.85,
             label="posterior of $p_B$", color="#467821", normed=True)
    plt.vlines(true_p_B, 0, 80, linestyle="--", label="true $p_B$ (unknown)")
    plt.legend(loc="upper right")

    ax = plt.subplot(313)
    plt.hist(delta_samples, histtype='stepfilled', bins=30, alpha=0.85,
             label="posterior of delta", color="#7A68A6", normed=True)
    plt.vlines(true_p_A - true_p_B, 0, 60, linestyle="--",
               label="true delta (unknown)")
    plt.vlines(0, 0, 60, color="black", alpha=0.2)
    plt.legend(loc="upper right")
    plt.show()

    # Count the number of samples less than 0, i.e. the area under the curve
    # before 0, represent the probability that site A is worse than site B.
    print "Probability site A is WORSE than site B: %.3f" % \
        (delta_samples < 0).mean()

    print "Probability site A is BETTER than site B: %.3f" % \
        (delta_samples > 0).mean()


if __name__ == '__main__':
    main()