from matplotlib import pyplot as plt
import numpy as np


def stock_loss(true_return, yhat, alpha=100.):
    if true_return * yhat < 0:
        # opposite signs, not good
        return alpha * yhat ** 2 - np.sign(true_return) * yhat \
            + abs(true_return)
    else:
        return abs(true_return - yhat)


def main():
    true_value = .05
    pred = np.linspace(-.04, .12, 75)

    plt.plot(pred, [stock_loss(true_value, _p) for _p in pred],
             label="Loss associated with\n prediction if true value = 0.05",
             lw=3)
    plt.vlines(0, 0, .25, linestyles="--")

    plt.xlabel("prediction")
    plt.ylabel("loss")
    plt.xlim(-0.04, .12)
    plt.ylim(0, 0.25)

    true_value = -.02
    plt.plot(pred, [stock_loss(true_value, _p) for _p in pred], alpha=0.6,
             label="Loss associated with\n prediction if true value = -0.02",
             lw=3)
    plt.legend()
    plt.title("Stock returns loss if true value = 0.05, -0.02")
    plt.show()


if __name__ == '__main__':
    main()
