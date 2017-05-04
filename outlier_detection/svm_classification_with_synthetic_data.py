import numpy as np
from   matplotlib import pyplot as plt
import matplotlib.font_manager
from   sklearn import svm


def main():
    tests = 20

    # Generate train data
    X = (np.random.randn(120, 2) * 
         np.array([0.08, 0.02]) + 
         np.array([0.3, 0.6]))

    X_train = X[:-tests]
    X_test = X[-tests:]
    X_outliers = np.copy(X_test)
    X_outliers = (X_outliers + 
        np.random.uniform(low=-0.1, high=0.1, size=(tests, 2)))

    # fit the model
    clf = svm.OneClassSVM(nu=0.1, kernel='rbf', gamma=0.1)
    clf.fit(X_train)

    y_pred_train = clf.predict(X_train)
    y_pred_test = clf.predict(X_test)
    y_pred_outliers = clf.predict(X_outliers)
    
    print(y_pred_test)
    print(y_pred_outliers)

    s = 40
    plt.scatter(X_train[:, 0], X_train[:, 1], c='white', s=s)
    plt.scatter(X_test[:, 0], X_test[:, 1], c='blueviolet', s=s)
    plt.scatter(X_outliers[:, 0], X_outliers[:, 1], c='gold', s=s)

    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    main()
