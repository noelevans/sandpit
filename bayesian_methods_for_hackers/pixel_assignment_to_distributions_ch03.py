import numpy as np
import pymc as pm
from scipy import stats


def main():
    data = np.loadtxt("data/mixture_data.csv", delimiter=",")

    p = pm.Uniform("p", 0, 1)

    assignment = pm.Categorical("assignment", [p, 1 - p], size=data.shape[0])

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

    # and to combine it with the observations:
    observations = pm.Normal("obs", center_i, tau_i, value=data, observed=True)

    # below we create a model class
    model = pm.Model([p, assignment, observations, taus, centers])

    mcmc = pm.MCMC(model)
    mcmc.sample(50000)

    p_trace = mcmc.trace("p")[:]
    center_trace = mcmc.trace("centers")[:]
    std_trace = mcmc.trace("stds")[:]
    x = 175

    v = ((p_trace *
          stats.norm.pdf(x, loc=center_trace[:, 0], scale=std_trace[:, 0]))
         >
         (1 - p_trace) *
          stats.norm.pdf(x, loc=center_trace[:, 1], scale=std_trace[:, 1]))

    print "Probability of belonging to cluster 1:", v.mean()
    print "Probability of belonging to cluster 0:", 1 - v.mean()


if __name__ == '__main__':
    main()
