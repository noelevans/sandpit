import datetime

import pandas as pd
from sklearn import preprocessing

from random_forest import RandomForestModel
from naive_bayes import NaiveBayesModel, BernoulliNaiveBayesModel


CATEGORICAL_VARS = ('DayOfWeek', 'PdDistrict')
TIME_SERIES_VARS = ('Date', 'Time')


def time_diff(start, end):
    dt_start = datetime.datetime.combine(datetime.date.today(), start)
    dt_end = datetime.datetime.combine(datetime.date.today(), end)
    return float((dt_end - dt_start).seconds) / (60 * 60)


def models():
    return [NaiveBayesModel(), BernoulliNaiveBayesModel()]
    # return [RandomForestModel(), NaiveBayesModel()]


class KaggleDataModel(object):

    def feature_engineering(self, filename, is_training=False):
        df = pd.read_csv(filename)
        temp = pd.DatetimeIndex(df['Dates'])
        df['Date'] = temp.date
        df['Time'] = temp.time

        # Rubbish or variables better engineered in another way
        del df['Dates']
        del df['Address']         # Removing just for now

        if is_training:
            encoders = {}
            for c in CATEGORICAL_VARS:
                all_choices = tuple(set(df[c]))
                le = preprocessing.LabelEncoder()
                le.fit(all_choices)
                encoders[c] = le
            for t in TIME_SERIES_VARS:
                encoders[t] = min(df[t])
                self.encoders = encoders

        for c in CATEGORICAL_VARS:
            df[c] = self.encoders[c].transform(df[c])
        for v in TIME_SERIES_VARS:
            if v == 'Date':
                df[v] = df[v].apply(lambda t: (t - self.encoders[v]).days)
            elif v == 'Time':
                df[v] = df[v].apply(lambda t: time_diff(self.encoders[v], t))

        if is_training:
            # df['Category'] = df['Category'].astype(object)

            # Omit when df$Y == 90 - seems to be a NA value
            df = df[df['Y'] != 90]

            del df['Descript']
            del df['Resolution']

        # Scaling coordinates so they are "prettier" to human-interpretation
        df['X'] = (df['X'] + 122) * 100
        df['Y'] = (df['Y'] -  37) * 100
        
        return df


    def load_training(self, training_filename):
        ''' For use with model_test_harness '''
        training = self.feature_engineering(training_filename, is_training=True)
        self.columns = list(training.ix[:,1:].columns)
        return training.ix[:,1:], training.ix[:,0]

    def trial_model(self):
        import lib_linear
        from sklearn.cross_validation import train_test_split
        
        Xs, y = sf_model.KaggleDataModel().load_training('train.csv')
        X_train, X_test, y_train, y_test = train_test_split(Xs, y, 
                                                            test_size=0.25)
        y_hat = lib_linear.NaiveBayesModel().model_and_predict()
        print sum(y_hat == y_test) / float(len(y_hat))
