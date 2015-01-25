""" Linear regression of annual change with simple mean averaged seasonality adjustments """

import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv('greenland-mass-change.csv')
    x = df['year']
    y = df['mass change']

    spline = interpolate.UnivariateSpline(x, y)
    yinterp = spline(x)
    best_fit_grad, best_fit_y_intercept = np.polyfit(x, y, 1)

    def best_fit_prediction(x):
        return best_fit_grad * x + best_fit_y_intercept

    best_fit = [best_fit_prediction(v) for v in x]

    train = df[df['year'] < 2012]
    test  = df[df['year'] > 2012]
    earliest = min(train['year'])
    latest = max(train['year'])

    predictions = []
    for n, t in enumerate(test['year']):
        start = (t - int(t)) + int(earliest)
        if start < earliest:
            start = start + 1
        end = (t - int(t)) + int(latest)
        if end > latest:
            end = end - 1
        steps = int(end - start)
        spline_samples = [spline(s + start) for s in range(steps)]
        relative_bases = [best_fit_prediction(s + start) for s in range(steps)]
        samples = [s - r for s, r in zip(spline_samples, relative_bases)]
        seasonal_mean = sum(samples) / len(samples)
        prediction = seasonal_mean + best_fit_prediction(t)
        if n == 7:
            test_xs = [(s + start) for s in range(steps)]
            test_ys = spline(test_xs)

        predictions.append(prediction)

    plt.plot(x, y, 'g.', label='Original')
    plt.plot(x, yinterp, 'm', label='Interpolated')
    # plt.plot(x, best_fit, 'c--', label='Regression')
    plt.plot(test['year'], predictions, 'ko', label='$P_{linear\ averaging}$')
    plt.plot(test_xs, test_ys, 'y^', label='Test points')

    plt.title('Greenland mass change')
    plt.xlabel('Time')
    plt.ylabel('Mass')
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.savefig('greenland-mass-change.png')

if __name__ == '__main__':
    main()
