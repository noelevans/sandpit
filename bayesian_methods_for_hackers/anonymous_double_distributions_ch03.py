from matplotlib import pyplot as plt
import numpy as np
import pymc as pm

from IPython.core.pylabtools import figsize


def main():
    figsize(12.5, 4)
    data = np.loadtxt("data/mixture_data.csv", delimiter=",")

    plt.hist(data, bins=20, color="k", histtype="stepfilled", alpha=0.8)
    plt.title("Histogram of the dataset")
    plt.ylim([0, None])
    print data[:10], "..."
    # plt.show()

    p = pm.Uniform("p", 0, 1)

    assignment = pm.Categorical("assignment", [p, 1 - p], size=data.shape[0])
    print "prior assignment, with p = %.2f:" % p.value
    print assignment.value[:10], "..."

    taus = 1.0 / pm.Uniform("stds", 0, 100, size=2) ** 2
    centers = pm.Normal("centers", [120, 190], [0.01, 0.01], size=2)

    """
    The below deterministic functions map an assignment, in this case 0 or 1,
    to a set of parameters, located in the (1,2) arrays `taus` and `centers`.
    """

    @pm.deterministic
    def center_i(assignment=assignment, centers=centers):
        return centers[assignment]

    @pm.deterministic
    def tau_i(assignment=assignment, taus=taus):
        return taus[assignment]

    print "Random assignments: ", assignment.value[:4], "..."
    print "Assigned center: ", center_i.value[:4], "..."
    print "Assigned precision: ", tau_i.value[:4], "..."

    observations = pm.Normal("obs", center_i, tau_i, value=data, observed=True)
    model = pm.Model([p, assignment, observations, taus, centers])

    mcmc = pm.MCMC(model)
    mcmc.sample(50000)

    plt.subplot(311)
    lw = 1
    center_trace = mcmc.trace("centers")[:]

    if center_trace[-1, 0] > center_trace[-1, 1]:
        colors = ["#348ABD", "#A60628"]
    else:
        colors = ["#A60628", "#348ABD"]

    plt.plot(center_trace[:, 0], label="trace of center 0", c=colors[0], lw=lw)
    plt.plot(center_trace[:, 1], label="trace of center 1", c=colors[1], lw=lw)
    plt.title("Traces of unknown parameters")
    leg = plt.legend(loc="upper right")
    leg.get_frame().set_alpha(0.7)

    plt.subplot(312)
    std_trace = mcmc.trace("stds")[:]
    plt.plot(std_trace[:, 0], label="trace of standard deviation of cluster 0",
         c=colors[0], lw=lw)
    plt.plot(std_trace[:, 1], label="trace of standard deviation of cluster 1",
         c=colors[1], lw=lw)
    plt.legend(loc="upper left")

    plt.subplot(313)
    p_trace = mcmc.trace("p")[:]
    plt.plot(p_trace, label="$p$: frequency of assignment to cluster 0",
         color="#467821", lw=lw)
    plt.xlabel("Steps")
    plt.ylim(0, 1)
    plt.legend()
    # plt.show()

    std_trace = mcmc.trace("stds")[:]

    # _i = [1, 2, 3, 4]
    _i = [1, 2, 3, 0]
    for i in range(2):
        plt.subplot(2, 2, _i[2 * i])
        plt.title("Posterior of center of cluster %d" % i)
        plt.hist(center_trace[:, i], color=colors[i], bins=30,
                 histtype="stepfilled")

        plt.subplot(2, 2, _i[2 * i + 1])
        plt.title("Posterior of standard deviation of cluster %d" % i)
        plt.hist(std_trace[:, i], color=colors[i], bins=30,
                 histtype="stepfilled")
        # plt.autoscale(tight=True)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
