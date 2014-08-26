import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_boston
from sklearn.cross_validation import KFold, cross_val_score
from sklearn import linear_model
from sklearn import svm
from sklearn import ensemble

import matplotlib.pyplot as plt


boston = load_boston()

X_train, X_test, y_train, y_test = train_test_split(boston.data,
                                                    boston.target,
                                                    test_size=0.25,
                                                    random_state=33)

scaler_x = StandardScaler().fit(X_train)
scaler_y = StandardScaler().fit(y_train)
X_train  = scaler_x.transform(X_train)
y_train  = scaler_y.transform(y_train)
X_test   = scaler_x.transform(X_test)
y_test   = scaler_y.transform(y_test)


def train_and_evaluate(classifier, x_training, y_training):
    """ Here the coefficient of determination is being calculated. It resembles
        a "How accurate is my model" number for comparison (where 1.0 is
        perfect). """
    classifier.fit(x_training, y_training)
    print "Coefficient of determination on training set:", classifier.score(x_training, y_training)
    # create a k-fold cross validation iterator of k=5 folds
    cv = KFold(x_training.shape[0], 5, shuffle=True, random_state=33)
    scores = cross_val_score(classifier, x_training, y_training, cv=cv)
    print "Average coefficient of determination using 5-fold cross-validation:", np.mean(scores)
    

clf_sgd = linear_model.SGDRegressor(loss='squared_loss', penalty=None, random_state=42)
train_and_evaluate(clf_sgd, X_train, y_train)

# print clf_sgd.coef_

# Now trying with a different penalty function. These penalise more complicated
# models so that over-fitting is less likely to occur
clf_sgd1 = linear_model.SGDRegressor(loss='squared_loss', penalty='l2', random_state=42)
train_and_evaluate(clf_sgd1, X_train, y_train)

clf_svr = svm.SVR(kernel='linear')
train_and_evaluate(clf_svr, X_train, y_train)

clf_svr_poly = svm.SVR(kernel='poly')
train_and_evaluate(clf_svr_poly, X_train, y_train)

clf_svr_rbf = svm.SVR(kernel='rbf')
train_and_evaluate(clf_svr_rbf, X_train, y_train)

# Perfect prediction in this data sample!
clf_et = ensemble.ExtraTreesRegressor(n_estimators=10, random_state=42)
train_and_evaluate(clf_et, X_train, y_train)

# Show the importance of each input variable. The most important being ZN and NOX
print sorted(zip(clf_et.feature_importances_, boston.feature_names))

