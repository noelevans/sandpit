"""
Position 300. Trend 145 up. Error 0.54616. Attempt 9. Wed, 27 Aug 2014 15:56:13

Your Best Entry
You improved on your best score by 0.34067.
You just moved up 175 positions on the leaderboard
"""

import datetime
import pandas as pd

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import ExtraTreesRegressor


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
    return df


def predict_for(output, cycles, tests, raw_tests, inputs):
    x_train, x_test, y_train, y_test = train_test_split(cycles[inputs],
                                                        cycles[output],
                                                        test_size=0.25,
                                                        random_state=33)
    scaler_x  = StandardScaler().fit(x_train)
    scaler_t  = StandardScaler().fit(tests)
    x_train   = scaler_x.transform(x_train)
    x_test    = scaler_x.transform(x_test)
    tests     = scaler_t.transform(tests)

    clf_et = ExtraTreesRegressor(n_estimators=10,
                                 compute_importances=True, random_state=42)
    clf_et.fit(x_train, y_train)

    ps = clf_et.predict(tests)
    return {dt: int(round(p)) for dt, p in zip(raw_tests['datetime'], ps)}


inputs = ['holiday', 'workingday', 'temp', 'atemp',
          'humidity', 'windspeed', 'month', 'hour']

cycles    = load_and_munge_training_data('train.csv')
raw_tests = load_and_munge_training_data('test.csv')
tests     = raw_tests[inputs]

casual     = predict_for('casual',     cycles, tests, raw_tests, inputs)
registered = predict_for('registered', cycles, tests, raw_tests, inputs)

for dt, cp in casual.items():
    print '%s,%i' % (dt, int(round(cp + registered[dt])))
