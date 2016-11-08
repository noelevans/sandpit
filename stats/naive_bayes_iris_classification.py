from __future__ import division

from sklearn import datasets
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split


def main():
    iris = datasets.load_iris()
    res = train_test_split(iris.data, iris.target,
        test_size=0.2, random_state=0)
    train_X, test_X, train_y, test_y = res

    gnb = GaussianNB()
    model = gnb.fit(train_X, train_y)
    y_hat = model.predict(test_X)

    tests = test_y.shape[0]
    fails = (test_y != y_hat).sum()
    print('Number of mislabeled points out of a total %d points : %d' %
        (tests, fails))
    print('Cost: %.2f' % (fails / tests))


if __name__ == '__main__':
    main()
