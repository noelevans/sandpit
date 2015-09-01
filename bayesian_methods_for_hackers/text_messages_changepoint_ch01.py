import matplotlib.pyplot as plt
import numpy as np
import pymc as pm


def main():

    count_data = np.loadtxt("txtdata.csv")
    n_count_data = len(count_data)

    alpha = 1.0 / count_data.mean()  # Recall count_data is the
                                   # variable that holds our txt counts
    lambda_1 = pm.Exponential("lambda_1", alpha)
    lambda_2 = pm.Exponential("lambda_2", alpha)

    tau = pm.DiscreteUniform("tau", lower=0, upper=n_count_data)

    @pm.deterministic
    def lambda_(tau=tau, lambda_1=lambda_1, lambda_2=lambda_2):
        out = np.zeros(n_count_data)
        out[:tau] = lambda_1  # lambda before tau is lambda1
        out[tau:] = lambda_2  # lambda after (and including) tau is lambda2
        return out

    observation = pm.Poisson("obs", lambda_, value=count_data, observed=True)

    model = pm.Model([observation, lambda_1, lambda_2, tau])

    # Mysterious code to be explained in Chapter 3.
    mcmc = pm.MCMC(model)
    mcmc.sample(40000, 10000, 1)

    lambda_1_samples = mcmc.trace('lambda_1')[:]
    lambda_2_samples = mcmc.trace('lambda_2')[:]
    tau_samples = mcmc.trace('tau')[:]

    print 'Exercises:'
    print 'Q1.a) lambda_1 mean:', lambda_1_samples.mean()
    print 'Q1.b) lambda_2 mean:', lambda_2_samples.mean()
    print 'Q2)   Percentage increase after Tau:',
    print 100 * sum(lambda_2_samples - lambda_1_samples) / sum(lambda_1_samples)
    print 'Q3)   ', lambda_1_samples[tau_samples < 45].mean()

    # End exercises

    # histogram of the samples:

    ax = plt.subplot(311)
    ax.set_autoscaley_on(False)

    plt.hist(lambda_1_samples, histtype='stepfilled', bins=30, alpha=0.85,
             label="posterior of $\lambda_1$", color="#A60628", normed=True)
    plt.legend(loc="upper left")
    plt.title(r"""Posterior distributions of the variables
        $\lambda_1,\;\lambda_2,\;\tau$""")
    plt.xlim([15, 30])
    plt.xlabel("$\lambda_1$ value")

    ax = plt.subplot(312)
    ax.set_autoscaley_on(False)
    plt.hist(lambda_2_samples, histtype='stepfilled', bins=30, alpha=0.85,
             label="posterior of $\lambda_2$", color="#7A68A6", normed=True)
    plt.legend(loc="upper left")
    plt.xlim([15, 30])
    plt.xlabel("$\lambda_2$ value")

    plt.subplot(313)
    w = 1.0 / tau_samples.shape[0] * np.ones_like(tau_samples)
    plt.hist(tau_samples, bins=n_count_data, alpha=1,
             label=r"posterior of $\tau$",
             color="#467821", weights=w, rwidth=2.)
    plt.xticks(np.arange(n_count_data))

    plt.legend(loc="upper left")
    plt.ylim([0, .75])
    plt.xlim([35, len(count_data) - 20])
    plt.xlabel(r"$\tau$ (in days)")
    plt.ylabel("probability")

    plt.show()


if __name__ == '__main__':
    main()