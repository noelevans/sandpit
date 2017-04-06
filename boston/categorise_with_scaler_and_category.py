import numpy as np
from   scipy import stats
from   sklearn import datasets
from   sklearn.linear_model import LogisticRegression
from   sklearn.naive_bayes import GaussianNB
from   sklearn.cross_validation import train_test_split


def get_predictors(dataset, field_names):
    fns = dataset.feature_names
    predictors = np.array(field_names)
    X_idx = np.in1d(fns, predictors)
    return dataset.data[:, X_idx]


def scaler_predictor(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=33)

    model = GaussianNB()
    model.fit(X_train, y_train)
    return model.predict_proba(y_test)


def categorical_predictor(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=33)

    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model.predict_proba(y_test)


def main():
    boston = datasets.load_boston()
    y = boston.target       # House prices
    mean = np.mean(y)
    y = y > mean            # y now means is_above_average_house_price
    y_train, y_test = train_test_split(y, test_size=0.25, random_state=33)

    scaler_predictors = [
        'NOX',              # Air concentration of nitrous-oxide
        'CRIM',             # Crime rate per capita
        ]
    scaler_X = get_predictors(boston, scaler_predictors)
    scaler_y_hat = scaler_predictor(scaler_X, y)

    cat_predictors = [
        'CHAS',             # Is district close to river
        ]
    cat_X = get_predictors(boston, cat_predictors)
    categorical_y_hat = categorical_predictor(cat_X, y)

    y_hat = scaler_y_hat * categorical_y_hat

    matches = y_hat == y_test
    print('Success rate: %i / %i = %f' % (
        matches.sum(), matches.size, float(matches.sum()) / matches.size))


if __name__ == '__main__':
    main()
