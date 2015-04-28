import math
import numpy as np
import pandas as pd
from scipy import interpolate, poly1d
import matplotlib.pyplot as plt
 
 
def rmse(targets, predictions):
    return np.sqrt(((targets - predictions) ** 2).mean())
   
 
def trend_curve(train_xs, train_ys):
    # Found 3 experimentally. See climate_change_analysis_polynomial_fit.py
    coefficients = np.polyfit(train_xs, train_ys, 3)
    return poly1d(coefficients)
   
 
def seasonal_curve(train_xs, train_ys):
    choice = 1
    if choice == 1:
        coefficients = np.polyfit(train_xs, train_ys, 1)
        return poly1d(coefficients)
    elif choice == 2:
        alpha = 0.2
        weights = [alpha * math.pow(1 - alpha, n) for n in range(len(train_ys))]
        weighted_sum = sum(t * w for t, w in zip(train_ys, reversed(weights)))
        average = weighted_sum / sum(weights)
        return lambda t: average
 
   
def main():
    df = pd.read_csv('greenland-mass-change.csv')
    all_xs = df['year']
    all_ys = df['mass change']
   
    train = df[df['year'] < 2012]
    test  = df[df['year'] > 2012]
    train_xs = train['year']
    train_ys = train['mass change']
    test_xs  = test['year']
    test_ys  = test['mass change']
 
    spline_fn = interpolate.UnivariateSpline(all_xs, all_ys)
 
    trend_fn = trend_curve(train_xs, train_ys)
    best_fit = trend_fn(all_xs)
 
    earliest = min(train_xs)
    latest = max(train_xs)
 
    predictions = []
    for n, t in enumerate(test_xs):
        start = (t - int(t)) + int(earliest)
        end = (t - int(t)) + int(latest)
        steps = [x for x in np.arange(start, end, 1) if earliest < x < latest]
       
        spline_samples = spline_fn(steps)
        trend = trend_fn(steps)
        N = 0
        if n == N:
            example_xs = steps
            example_ys = spline_samples
            print spline_samples
            print trend
            print spline_samples / trend
            print '....'
            print trend / spline_samples
            print np.mean(trend / spline_samples)
            print trend_fn(t)
            print '....'
 
        samples = trend / spline_samples
       
        # seasonal_fn = seasonal_curve(steps, samples)
        # prediction = trend_fn(t) * seasonal_fn(t)

        prediction = trend_fn(t) * np.mean(trend / spline_samples)
       
 
       
        predictions.append(prediction)
       
    print rmse(test_ys, predictions)
 
    plt.plot(all_xs, all_ys, 'bo', label='Original', fillstyle='none')
    plt.plot(all_xs, spline_fn(all_xs), 'b-')
    plt.plot(all_xs, best_fit, 'c--', label='Regression')
    plt.plot(test_xs[:1], predictions[:1], 'ko', label='$P_{linear\ averaging}$')
    plt.plot(example_xs, example_ys, marker='o', color='orange', label='7s')
   
    plt.title('Greenland mass change')
    plt.xlabel('Time')
    plt.ylabel('Mass')
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.savefig('greenland-mass-change.png')
 
 
if __name__ == '__main__':
    main()