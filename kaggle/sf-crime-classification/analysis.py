import datetime
import optparse

import numpy as np
import pandas as pd

from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier

# Dependent variables to resolve:
# Address -> Break somehow
# Resolution ???

CATEGORICAL_VARS = ('DayOfWeek', 'PdDistrict')
TIME_SERIES_VARS = ('Date', 'Time')
OUT_COL_NAMES = ("ARSON", "ASSAULT", "BAD CHECKS", "BRIBERY", "BURGLARY",
                 "DISORDERLY CONDUCT", "DRIVING UNDER THE INFLUENCE",
                 "DRUG/NARCOTIC", "DRUNKENNESS", "EMBEZZLEMENT", "EXTORTION",
                 "FAMILY OFFENSES", "FORGERY/COUNTERFEITING", "FRAUD",
                 "GAMBLING", "KIDNAPPING", "LARCENY/THEFT", "LIQUOR LAWS",
                 "LOITERING", "MISSING PERSON", "NON-CRIMINAL",
                 "OTHER OFFENSES", "PORNOGRAPHY/OBSCENE MAT", "PROSTITUTION",
                 "RECOVERED VEHICLE", "ROBBERY", "RUNAWAY", "SECONDARY CODES",
                 "SEX OFFENSES FORCIBLE", "SEX OFFENSES NON FORCIBLE",
                 "STOLEN PROPERTY", "SUICIDE", "SUSPICIOUS OCC", "TREA",
                 "TRESPASS", "VANDALISM", "VEHICLE THEFT", "WARRANTS",
                 "WEAPON LAWS")


def time_diff(start, end):
    dt_start = datetime.datetime.combine(datetime.date.today(), start)
    dt_end = datetime.datetime.combine(datetime.date.today(), end)
    return float((dt_end - dt_start).seconds) / (60 * 60)


def feature_engineering(filename, is_training=False, encoders=None):
    df = pd.read_csv(filename)
    temp = pd.DatetimeIndex(df['Dates'])
    df['Date'] = temp.date
    df['Time'] = temp.time

    # Rubbish or variables better engineered in another way
    del df['Dates']
    del df['Address']         # Removing just for now

    if not encoders:
        encoders = {}
        for c in CATEGORICAL_VARS:
            all_choices = tuple(set(df[c]))
            le = preprocessing.LabelEncoder()
            le.fit(all_choices)
            encoders[c] = le
        for t in TIME_SERIES_VARS:
            encoders[t] = min(df[t])

    for c in CATEGORICAL_VARS:
        df[c] = encoders[c].transform(df[c])
    for v in TIME_SERIES_VARS:
        if v == 'Date':
            df[v] = df[v].apply(lambda t: (t - encoders[v]).days)
        elif v == 'Time':
            df[v] = df[v].apply(lambda t: time_diff(encoders[v], t))

    if is_training:
        # df['Category'] = df['Category'].astype(object)

        # Omit when df$Y == 90 - seems to be a NA value
        df = df[df['Y'] != 90]

        del df['Descript']
        del df['Resolution']

    # Scaling coordinates so they are "prettier" to human-interpretation
    df['X'] = (df['X'] + 122) * 100
    df['Y'] = (df['Y'] -  37) * 100

    return df, encoders


class RandomForestModel(object):

    def __init__(self, full_run=False):
        if full_run:
            self.n_trees = 60
        else:
            self.n_trees = 1


    def load_training(self, training_filename):
        ''' For use with model_test_harness '''
        training, _ = feature_engineering(training_filename, is_training=True)
        self.columns = list(training.ix[:,1:].columns)
        return training.ix[:,1:], training.ix[:,0]


    def model_and_predict(self, X_train, y_train, X_test):
        district_idx = self.columns.index('PdDistrict')
        districts = set(X_train[:,district_idx])
        district_ys = {}
        # Grow forest and predict separately for each district's records
        for d in districts:
            district_X_train = X_train[X_train[:, district_idx] == d]
            district_X_train = np.delete(district_X_train, district_idx, 1)
            district_y_train = y_train[X_train[:, district_idx] == d]
            district_X_test = X_test[X_test[:, district_idx] == d]
            district_X_test = np.delete(district_X_test, district_idx, 1)
            print "Growing forest for", d

            # Not saving output in Git so make this deterministic 
            # with random_state
            rf = RandomForestClassifier(n_estimators=self.n_trees, n_jobs=-1,
                                        random_state=782629)
            rf.fit(district_X_train, district_y_train)

            district_ys[d] = list(rf.predict(district_X_test))
            print "Finished", d

        print "All predictions made"

        y_hat = []
        for row in X_test:
            d_ys = district_ys[row[district_idx]]
            y_hat.append(d_ys.pop(0))

        return y_hat


def build_model():
    return RandomForestModel()


def main():
    parser = optparse.OptionParser()

    parser.add_option('--full', action='store_true', default=False)
    options, _ = parser.parse_args()

    if options.full:
        print "Running full execution of training/test data"
        train_filename = "train.csv"
        test_filename = "test.csv"
        independent_vars = ['DayOfWeek', 'Date', 'Time', 'X', 'Y']
        n_trees = 1
    else:
        print "Running with a subset of training/test data"
        train_filename = "train.small.csv"
        test_filename = "test.small.csv"
        independent_vars = ['DayOfWeek', 'Date', 'Time', 'X', 'Y']
        n_trees = 1


    train, encoders = feature_engineering(train_filename, is_training=True)
    test, _ = feature_engineering(test_filename, encoders=encoders)
    
    ys = model_and_predict(training.ix[:,1:], training.ix[:,0])

    # Build output CSV format
    true_indicies = [OUT_COL_NAMES.index(y) for y in ys]
    result_row = lambda pos: [int(i == pos) for i in range(len(OUT_COL_NAMES))]
    out_df = pd.DataFrame([result_row(i) for i in true_indicies])
    out_df.to_csv('submission.csv', header=OUT_COL_NAMES, index_label='Id')


if __name__ == '__main__':
    main()