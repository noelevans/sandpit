import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
import pymc as pm
from scipy import stats

from IPython.core.pylabtools import figsize


def main():
    figsize(12.5, 4)
    data = np.loadtxt("data/mixture_data.csv", delimiter=",")

    plt.hist(data, bins=20, color="k", histtype="stepfilled", alpha=0.8)
    plt.title("Histogram of the dataset")
    plt.ylim([0, None])
    print data[:10], "..."
    plt.show()

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
    plt.show()

    std_trace = mcmc.trace("stds")[:]

    _i = [1, 2, 3, 4]
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

    plt.cmap = mpl.colors.ListedColormap(colors)
    plt.imshow(mcmc.trace("assignment")[::400, np.argsort(data)],
           cmap=plt.cmap, aspect=.4, alpha=.9)
    plt.xticks(np.arange(0, data.shape[0], 40),
           ["%.2f" % s for s in np.sort(data)[::40]])
    plt.ylabel("posterior sample")
    plt.xlabel("value of $i$th data point")
    plt.title("Posterior labels of data points")
    plt.show()

    cmap = mpl.colors.LinearSegmentedColormap.from_list("BMH", colors)
    assign_trace = mcmc.trace("assignment")[:]
    plt.scatter(data, 1 - assign_trace.mean(axis=0), cmap=cmap,
            c=assign_trace.mean(axis=0), s=50)
    plt.ylim(-0.05, 1.05)
    plt.xlim(35, 300)
    plt.title("Probability of data point belonging to cluster 0")
    plt.ylabel("probability")
    plt.xlabel("value of data point")
    plt.show()

    x = np.linspace(20, 300, 500)
    posterior_center_means = center_trace.mean(axis=0)
    posterior_std_means = std_trace.mean(axis=0)
    posterior_p_mean = mcmc.trace("p")[:].mean()

    plt.hist(data, bins=20, histtype="step", normed=True, color="k",
         lw=2, label="histogram of data")
    y = posterior_p_mean * stats.norm.pdf(x, loc=posterior_center_means[0],
                                    scale=posterior_std_means[0])
    plt.plot(x, y, label="Cluster 0 (using posterior-mean parameters)", lw=3)
    plt.fill_between(x, y, color=colors[1], alpha=0.3)

    y = (1 - posterior_p_mean) * stats.norm.pdf(x, loc=posterior_center_means[1],
                                          scale=posterior_std_means[1])
    plt.plot(x, y, label="Cluster 1 (using posterior-mean parameters)", lw=3)
    plt.fill_between(x, y, color=colors[0], alpha=0.3)

    plt.legend(loc="upper left")
    plt.title("Visualizing Clusters using posterior-mean parameters")
    plt.show()


if __name__ == '__main__':
    main()
