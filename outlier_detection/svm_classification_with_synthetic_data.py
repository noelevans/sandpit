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

    # xx, yy = np.meshgrid(np.linspace(-5, 5, 500), np.linspace(-5, 5, 500))
    # # Function defining the decision boundary
    # Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    # Z = Z.reshape(xx.shape)

    pos_mask = y_pred_outliers ==  1
    neg_mask = y_pred_outliers == -1
    X_outliers_pos = X_outliers[pos_mask[: np.newaxis].T]
    X_outliers_neg = X_outliers[neg_mask[: np.newaxis].T]
    
    s = 40
    plt.scatter(X_train[:, 0], X_train[:, 1], c='white', s=s, label='Train')
    plt.scatter(X_test[:, 0], X_test[:, 1], c='black', s=s, label='Test')
    plt.scatter(X_outliers_pos[:, 0], X_outliers_pos[:, 1], c='#56B4E9', s=s, 
        label='Synthetic valid')
    plt.scatter(X_outliers_neg[:, 0], X_outliers_neg[:, 1], c='#F0E442', s=s,
        label='Synthetic invalid')
    # plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='darkred', 
    #     label='Learned frontier')
    
    plt.legend()
    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    main()
