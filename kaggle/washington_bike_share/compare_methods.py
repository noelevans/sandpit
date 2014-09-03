import datetime
import numpy as np
import pandas as pd
import operator
import pprint


from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn import linear_model
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.linear_model import LinearRegression


def normalise(df, normalise=[]):
    mins  = dict((field, min(df[field])) for field in normalise)
    maxes = dict((field, max(df[field])) for field in normalise)
                
    for field in normalise:
        f = lambda x: float(x - mins[field]) / (maxes[field] - mins[field])
        df[field] = map(f, df[field])
        
    return df


def load_and_munge_training_data(filename):
    
    parse_hour = lambda dt: int(dt.split()[1].split(':')[0])
    parse_month = lambda dt: int(dt.split()[0].split('-')[1])
    parse_day_of_week = lambda dt: parse_date(dt).weekday()
    
    def parse_date(dt): 
        return datetime.date(*(int(x) for x in dt.split()[0].split('-')))
        
    def parse_day_of_year(dt):
        _date = parse_date(dt)
        year_start = datetime.date(_date.year, 1, 1)
        return (_date - year_start).days
        
    df = pd.read_csv(open(filename))
    df['hour']  = map(parse_hour, df['datetime'])
    df['month'] = map(parse_month, df['datetime'])
    df['day_of_year'] = map(parse_day_of_year, df['datetime'])
    df['day_of_week'] = map(parse_day_of_week, df['datetime'])
    # return normalise(df, INPUT_FIELDS)
    return df


def coefficient_of_determination(clf, x_training, y_training):
    return clf.score(x_training, y_training)


def mean_coeffient_of_determination(clf, x_training, y_training):
    """Mean coefficient of determination using 5-fold crossvalidation: """
    cv = KFold(x_training.shape[0], 5, shuffle=True)
    scores = cross_val_score(clf, x_training, y_training, cv=cv)
    return np.mean(scores)


def evaluate(classifier, x_training, y_training):
    return (coefficient_of_determination(classifier, x_training, y_training),
            mean_coeffient_of_determination(classifier,
                                            x_training,
                                            y_training))


def run():
    cycles = load_and_munge_training_data('train.csv')
    inputs = ['holiday', 'workingday', 'temp', 'atemp',
              'humidity', 'windspeed', 'month', 'hour']

    x_train, x_test, y_train, y_test = train_test_split(cycles[inputs],
                                                        cycles['count'],
                                                        test_size=0.25)
    scaler_x = StandardScaler().fit(x_train)
    scaler_y = StandardScaler().fit(y_train)
    x_train  = scaler_x.transform(x_train)
    y_train  = scaler_y.transform(y_train)
    x_test   = scaler_x.transform(x_test)
    y_test   = scaler_y.transform(y_test)

    techniques = {}

    clf_sgd = linear_model.SGDRegressor(loss='squared_loss', penalty=None)
    clf_sgd.fit(x_train, y_train)
    techniques['Linear - no penalty'] = evaluate(clf_sgd, x_train, y_train)

    clf_sgd1 = linear_model.SGDRegressor(loss='squared_loss', penalty='l2')
    clf_sgd1.fit(x_train, y_train)
    techniques['Linear - squared sums of the coefficients penalisation'] = \
        evaluate(clf_sgd1, x_train, y_train)

    clf_svr = svm.SVR(kernel='linear')
    clf_svr.fit(x_train, y_train)
    techniques['SVR - linear'] = evaluate(clf_svr, x_train, y_train)

    clf_svr_poly = svm.SVR(kernel='poly')
    clf_svr_poly.fit(x_train, y_train)
    techniques['SVR - poly'] = evaluate(clf_svr_poly, x_train, y_train)

    clf_svr_rbf = svm.SVR(kernel='rbf')
    clf_svr_rbf.fit(x_train, y_train)
    techniques['SVR - RBF'] = evaluate(clf_svr_rbf, x_train, y_train)

    clf_et = ExtraTreesRegressor(n_estimators=10, compute_importances=True)
    clf_et.fit(x_train, y_train)
    techniques['Random forest'] = evaluate(clf_et, x_train, y_train)

    clf_lr = LinearRegression()
    clf_lr.fit(x_train, y_train)
    techniques['Linear regression'] = evaluate(clf_lr, x_train, y_train)

    return sorted(techniques.iteritems(), key=operator.itemgetter(1))

if __name__ == '__main__':
    pprint.pprint(run())
