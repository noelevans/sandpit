import json

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
import pymc as pm


def main():
    matplotlibrc_path = '/home/noel/repo/playground/matplotlibrc.json'
    matplotlib.rcParams.update(json.load(open(matplotlibrc_path)))

    lambda_1 = pm.Exponential("lambda_1", 1)  # prior on first behaviour
    lambda_2 = pm.Exponential("lambda_2", 1)  # prior on second behaviour
    tau = pm.DiscreteUniform("tau", lower=0, upper=10)  # prior on behaviour change

    print "lambda_1.value = %.3f" % lambda_1.value
    print "lambda_2.value = %.3f" % lambda_2.value
    print "tau.value = %.3f" % tau.value
    print

    lambda_1.random(), lambda_2.random(), tau.random()

    print "After calling random() on the variables..."
    print "lambda_1.value = %.3f" % lambda_1.value
    print "lambda_2.value = %.3f" % lambda_2.value
    print "tau.value = %.3f" % tau.value

    samples = [lambda_1.random() for i in range(20000)]
    plt.hist(samples, bins=70, normed=True, histtype="stepfilled")
    plt.title("Prior distribution for $\lambda_1$")
    plt.xlim(0, 8)
    plt.show()

    data = np.array([10, 5])
    fixed_variable = pm.Poisson("fxd", 1, value=data, observed=True)
    print "value: ", fixed_variable.value
    print "calling .random()"
    fixed_variable.random()
    print "value: ", fixed_variable.value

    n_data_points = 5  # in CH1 we had ~70 data points

    @pm.deterministic
    def lambda_(tau=tau, lambda_1=lambda_1, lambda_2=lambda_2):
        out = np.zeros(n_data_points)
        out[:tau] = lambda_1  # lambda before tau is lambda1
        out[tau:] = lambda_2  # lambda after tau is lambda2
        return out

    data = np.array([10, 25, 15, 20, 35])
    obs = pm.Poisson("obs", lambda_, value=data, observed=True)

    model = pm.Model([obs, lambda_, lambda_1, lambda_2, tau])


if __name__ == '__main__':
    main()
