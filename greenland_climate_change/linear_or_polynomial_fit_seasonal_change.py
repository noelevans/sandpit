import numpy as np
import pandas as pd
from scipy import interpolate, poly1d
import matplotlib.pyplot as plt
 
   
def main():
    df = pd.read_csv('greenland-mass-change.csv')
    all_xs = df['year']
    all_ys = df['mass change']
   
    train = df[df['year'] < 2012]
    test  = df[df['year'] > 2012]
    train_xs = train['year']
    train_ys = train['mass change']
    test_xs  = test['year']
 
    spline = interpolate.UnivariateSpline(all_xs, all_ys)
 
    # Found 3 experimentally. See climate_change_analysis_polynomial_fit.py
    coefficients = np.polyfit(train_xs, train_ys, 3)
    trend_fn = poly1d(coefficients)
 
    earliest = min(train['year'])
    latest = max(train['year'])
 
    seasonal_fluctuations = []
    for n, t in enumerate(test_xs):
        start = (t - int(t)) + int(earliest)
        if start < earliest:
            start = start + 1
        end = (t - int(t)) + int(latest)
        if end > latest:
            end = end - 1
        steps = [(s + start) for s in range(int(end - start))]
        spline_samples = [spline(s) for s in steps]
        relative_trend = trend_fn(steps)
        samples = [s - r for s, r in zip(spline_samples, relative_trend)]
           
        seasonal_fluctuations.append((samples, steps))
 
    for n, (f, s) in enumerate(seasonal_fluctuations):
        plt.plot(s, f)
   
    plt.title('Greenland mass change')
    plt.xlabel('Time')
    plt.ylabel('Mass')
    plt.grid(True)
    plt.show()
    plt.savefig('greenland-mass-change.png')
 
if __name__ == '__main__':
    main()
