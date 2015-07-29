import datetime
import numpy as np
import pandas as pd
from sklearn import preprocessing

from random_forest import RandomForestModel
from naive_bayes import NaiveBayesModel, BernoulliNaiveBayesModel


CATEGORICAL_VARS = ('DayOfWeek', 'PdDistrict', 'Address') #, 'Block', 'Junction_min', 
                    #'Junction_max')
TIME_SERIES_VARS = ('Date', 'Time') #, 'Dates')


def time_diff(start, end):
    dt_start = datetime.datetime.combine(datetime.date.today(), start)
    dt_end = datetime.datetime.combine(datetime.date.today(), end)
    return float((dt_end - dt_start).seconds) / (60 * 60)


def models():
    return [NaiveBayesModel(), BernoulliNaiveBayesModel()]


class KaggleDataModel(object):

    def feature_engineering(self, train_filename=None, test_filename=None):
        df = pd.read_csv(train_filename and train_filename or test_filename)
        temp = pd.DatetimeIndex(df['Dates'])
        df['Date'] = temp.date
        df['Time'] = temp.time
        del df['Dates']     # df['Dates'] = pd.to_datetime(df['Dates'])

        # df['Block'] = 'Block of' in df['Address'] and df['Address'] or ''
        # df['Junction_min'] =  ' / ' in df['Address'] and \
        #         min(df['Address'].split(' / ')) or ''
        # df['Junction_max'] =  ' / ' in df['Address'] and \
        #         max(df['Address'].split(' / ')) or ''
        
        # There are df['Y'] == 90 in the test set too. In this case, we 
        # guess the Y value by find others with the same road Address and 
        # take an average. Where there are no other same address crimes we 
        # just use 90 still
        # df_temp = df.copy(deep=True)
        # for n, row in df.iterrows():
        #     if row['Y'] == 90:
        #         same_addresses = df[df['Address'] == row['Address']]
        #         x_median = np.median(same_addresses['X'])
        #         y_median = np.median(same_addresses['Y'])
        #         df_temp['X'][n] = x_median
        #         df_temp['Y'][n] = y_median
        # df = df_temp

        if train_filename:
            encoders = {}
            for c in CATEGORICAL_VARS:
                all_choices = set(df[c])
                if c == 'Address':
                    test_choices = set(pd.read_csv(test_filename)['Address'])
                    all_choices = all_choices.union(test_choices) 
                le = preprocessing.LabelEncoder()
                le.fit(tuple(all_choices))
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
            elif v == 'Dates':
                f = lambda t: (t - self.encoders[v]).total_seconds() / (60*60.)
                df[v] = df[v].apply(f)

        if train_filename:
            # Omit when df['Y'] == 90 - seems to be a NA value
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
