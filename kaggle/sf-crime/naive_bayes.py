import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB, BernoulliNB

import sf_model


class NaiveBayesModel(object):

    def model_and_predict(self, X_train, y_train, X_test):
        nb = GaussianNB()
        nb.fit(X_train, y_train)
        return nb.predict(X_test)


class BernoulliNaiveBayesModel(object):

    def model_and_predict(self, X_train, y_train, X_test):
        nb = BernoulliNB()
        nb.fit(X_train, y_train)
        return nb.predict(X_test)


def main():
    train_filename = 'train.csv'
    test_filename = 'test.csv'
    data_prep = sf_model.KaggleDataModel()
    train = data_prep.feature_engineering(train_filename, test_filename)
    test  = data_prep.feature_engineering(test_filename=test_filename)

    Xs = train.ix[:,1:]
    y  = train.ix[:,0]
    model = GaussianNB()
    model.fit(Xs, y)
    y_hats = model.predict(test.ix[:,1:])

    # this line takes predictions [3, 3, 2] and transposes it with a 
    # necessary addition of a 2nd axis to make it [[3],
    #                                              [3],
    #                                              [2]]
    # Necessary to apply the equals test col_names == y_hats
    y_hats = y_hats[np.newaxis].T

    col_names = np.sort(train['Category'].unique())
    binary_matches = col_names == y_hats
    output = pd.DataFrame(binary_matches, columns=col_names)

    output['Id'] = test['Id'].astype(int)
    output = output[['Id'] + list(col_names)]
    output.to_csv('output.csv', index=False)


if __name__ == '__main__':
    main()