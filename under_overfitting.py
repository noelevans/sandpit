import numpy as np
from matplotlib import pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import cross_val_score


def main():
    np.random.seed(0)
    
    n_samples = 30
    true_fn = lambda X: np.cos(1.5 * np.pi * X)
    X = np.sort(np.random.rand(n_samples))
    y = true_fn(X) + np.random.randn(n_samples) * 0.1

    mses = []
    stds = []
    pipelines = []
    degrees = range(1, 16)

    # continuous_X = np.linspace(0, 1, 500)
    # plt.plot(continuous_X, true_fn(continuous_X), 
    #     c='aquamarine', label='Signal')
    # plt.scatter(X, y, label='Samples')
    # plt.title('Signal and noisy samples taken')
    # plt.legend()
    # plt.show()
    # return

    for d in degrees:
        poly_features = PolynomialFeatures(degree=d, include_bias=False)
        model = LinearRegression()
        pipeline = Pipeline([('polynomial_features', poly_features),
                             ('linear_regression', model)])
        pipeline.fit(X[:, np.newaxis], y)

        scores = cross_val_score(pipeline, X[:, np.newaxis], y,
                                 scoring='mean_squared_error', cv=10)

        print('Degree {:>2}: mse = {:16.3f}, std = {:16.3f}'.format(
            d, -scores.mean(), scores.std()))
        mses.append(-scores.mean())
        stds.append(scores.std())
        pipelines.append(pipeline)
    
    if False:
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.plot(degrees, mses, label='MSE', color='cornflowerblue')
        ax2.plot(degrees, stds, label='Sigma', color='teal')
        ax1.set_yscale('log')
        ax2.set_yscale('log')
        ax1.set_xlabel('Degrees')
        ax1.set_ylabel('Mean sq error', color='cornflowerblue')
        ax2.set_ylabel('Std deviation', color='teal')
        plt.title('Approximating noisy signal varying polynomial coefficients')
    else:
        height = 4
        width = 4
        n = 0
        fig, axs = plt.subplots(height, width)

        for h in range(height):
            for w in range(width):
                ax = axs[h, w]
                ax.set_xticklabels([])
                ax.set_yticklabels([])
                if h == w == 0:
                    ax.set_title('Raw data', fontsize=10)
                    ax.scatter(X, y, color='teal', s=7)
                else:
                    p = pipelines[n]
                    n += 1
                    ax.set_title('{} degrees'.format(n), fontsize=10)
                    ax.plot(X, p.predict(X[:, np.newaxis]), color='teal')
        plt.suptitle('Plots varying degrees of coefficients for independent')
    plt.show()


if __name__ == '__main__':
    main()
