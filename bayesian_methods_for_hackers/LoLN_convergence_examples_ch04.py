import numpy as np
import matplotlib.pyplot as plt
import pymc as pm


def main():
    sample_size = 100000
    expected_value = lambda_ = 4.5
    N_samples = range(1, sample_size, 100)

    for k in range(3):
        samples = pm.rpoisson(lambda_, size=sample_size)
        partial_average = [samples[:i].mean() for i in N_samples]
        label = "average of  $n$ samples; seq. %d" % k
        plt.plot(N_samples, partial_average, lw=1.5, label=label)

    plt.plot(N_samples, expected_value * np.ones_like(partial_average),
             ls="--", label="true expected value", c="k")

    plt.ylim(4.35, 4.65)
    plt.title("Convergence of the average of \n random variables to its" +
              "expected value")
    plt.ylabel("average of $n$ samples")
    plt.xlabel("# of samples, $n$")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
