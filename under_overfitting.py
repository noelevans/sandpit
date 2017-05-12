import numpy as np
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
    

if __name__ == '__main__':
    main()
