""" Analysis of best polynomial to fit to Greenland data """

import numpy as np
import pandas as pd
from scipy import poly1d
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv('greenland-mass-change.csv')
    xs = df['year']
    ys = df['mass change']

    def model(n=3):
        coefficients = np.polyfit(xs, ys, n)
        polynomial = poly1d(coefficients)
        return polynomial(xs)

    plt.plot(xs, ys, 'g.', label='Original')

    # model(1) is linear regression - the primary school best fit
    # 2 is a little bit different to the other two curves
    # 4 is an insignificant improvement on 3 so not worth the expense

    plt.plot(xs, model(1), label='Regression-1')
    plt.plot(xs, model(2), label='Regression-2')
    plt.plot(xs, model(3), label='Regression-3')
    plt.plot(xs, model(4), label='Regression-4')

    plt.title('Greenland mass change')
    plt.xlabel('Time')
    plt.ylabel('Mass')
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.savefig('greenland-mass-change-polynomials.png')

if __name__ == '__main__':
    main()
