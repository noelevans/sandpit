import numpy as np
import pandas as pd
from scipy import interpolate, poly1d
import matplotlib.pyplot as plt
 
 
def rmse(targets, predictions):
    return np.sqrt(((targets - predictions) ** 2).mean())
   
    
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
 
    spline = interpolate.UnivariateSpline(all_xs, all_ys)
    yinterp = spline(all_xs)
 
    # Found 3 experimentally. See climate_change_analysis_polynomial_fit.py
    coefficients = np.polyfit(train_xs, train_ys, 3)
    polynomial = poly1d(coefficients)
    best_fit = polynomial(all_xs)
 
    earliest = min(train['year'])
    latest = max(train['year'])
 
    predictions = []
    for t in test_xs:
        start = (t - int(t)) + int(earliest)
        if start < earliest:
            start = start + 1
        end = (t - int(t)) + int(latest)
        if end > latest:
            end = end - 1
        steps = [(s + start) for s in range(int(end - start))]
        spline_samples = [spline(s) for s in steps]
        relative_bases = polynomial(steps)
        samples = [s - r for s, r in zip(spline_samples, relative_bases)]
        seasonal_mean = sum(samples) / len(samples)
        prediction = seasonal_mean + polynomial(t)
 
        predictions.append(prediction)
       
    print rmse(test_ys, predictions)
 
    plt.plot(all_xs, all_ys, 'bo', label='Original', fillstyle='none')
    plt.plot(all_xs, yinterp, 'b-')
    plt.plot(all_xs, best_fit, 'c--', label='Regression')
    plt.plot(test_xs, predictions, 'ko', label='$P_{linear\ averaging}$')
   
    # plt.title('Greenland mass change')
    plt.xlabel('Time')
    plt.ylabel('Mass')
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.savefig('greenland-mass-change.png')
 
if __name__ == '__main__':
    main()