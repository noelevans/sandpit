import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt


def main():
    x  = np.linspace(-4, 4, 100)
    noise = np.random.normal(0, 0000.1, 100)
    y  = np.sin(x) + noise
    yinterp = interpolate.UnivariateSpline(x, y, s = 5e8)(x)
    plt.plot(x, y, 'o', label = 'Original')
    plt.plot(x, yinterp, 'r', label = 'Interpolated')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()