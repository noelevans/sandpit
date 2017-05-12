import numpy as np
from matplotlib import pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import cross_val_score


def main():
    np.random.seed(0)
    
    n_samples = 30
    degrees = range(1, 16)

    true_fn = lambda X: np.cos(1.5 * np.pi * X)
    X = np.sort(np.random.rand(n_samples))
    y = true_fn(X) + np.random.randn(n_samples) * 0.1

    mses = []
    stds = [] 

    for d in degrees:
        poly_features = PolynomialFeatures(degree=d, include_bias=False)
        model = LinearRegression()
        pipeline = Pipeline([('polynomial_features', poly_features),
                             ('linear_regression', model)])
        pipeline.fit(X[:, np.newaxis], y)

        scores = cross_val_score(pipeline, X[:, np.newaxis], y,
                                 scoring='mean_squared_error', cv=10)

        print('Degree {:>2}: mse = {}, std = {}'.format(
            d, -scores.mean(), scores.std()))
        mses.append(-scores.mean())
        stds.append(scores.std())
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.plot(degrees, mses, label='MSE', color='cornflowerblue')  
    ax2.plot(degrees, stds, label='Sigma', color='teal')
    ax1.set_yscale('log')
    ax2.set_yscale('log')
    ax1.set_xlabel('Coefficients / degrees')
    ax1.set_ylabel('Mean sq error', color='cornflowerblue')
    ax2.set_ylabel('Std deviation', color='teal')
    plt.title('Approximate noisy signal with varying number of degrees')
    plt.show()    

if __name__ == '__main__':
    main()
