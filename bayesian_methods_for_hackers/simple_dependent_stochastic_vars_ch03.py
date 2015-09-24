from matplotlib import pyplot as plt
import pymc as pm


def main():
    x = pm.Normal("x", 4, 10)
    y = pm.Lambda("y", lambda x=x: 10 - x, trace=True)

    ex_mcmc = pm.MCMC(pm.Model([x, y]))
    ex_mcmc.sample(500)

    plt.plot(ex_mcmc.trace("x")[:])
    plt.plot(ex_mcmc.trace("y")[:])
    plt.title("Displaying (extreme) case of dependence between unknowns")
    plt.show()


if __name__ == '__main__':
    main()
