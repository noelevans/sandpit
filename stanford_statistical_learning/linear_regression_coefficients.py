import numpy as np
import sklearn.datasets

import plotly.plotly as py
from plotly.graph_objs import Scatter, Data


def main():
    vars = sklearn.datasets.load_boston()['feature_names']
    boston = sklearn.datasets.load_boston()['data']
    X_idx = np.where(vars == 'DIS')[0][0]
    Y_idx = np.where(vars == 'NOX')[0][0]
    X = boston[:, X_idx]
    Y = boston[:, Y_idx]
    
    X_mean = np.mean(X)
    Y_mean = np.mean(Y)
    
    # See Introduction to Statistical Learning Ch 3.1 (Fig 3.4)
    numer = sum((x - X_mean) * (y - Y_mean) for x, y in zip(X, Y))
    denom = sum((x - X_mean) ** 2 for x, y in zip(X, Y))
    beta_1 = numer / denom
    beta_0 = Y_mean - beta_1 * X_mean
    eqn = 'Y(hat) = %.3f %f.3x' % (beta_0, beta_1)
    
    print 'Determined the below line of best fit...'
    print eqn

    trace = Scatter(x=X, y=Y, mode='markers')
    name = 'Determined this regression: %s' % eqn
    plot_url = py.plot(Data([trace]), filename=name)

if __name__ == '__main__':
    main()
