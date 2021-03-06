import datetime
import numpy as np
import pandas as pd
from sklearn import preprocessing

from random_forest import RandomForestModel
from naive_bayes import NaiveBayesModel, BernoulliNaiveBayesModel


CATEGORICAL_VARS = ('DayOfWeek', 'PdDistrict', 'Address') #, 'Block', 
                    # 'Junction_min', 'Junction_max')
TIME_SERIES_VARS = ('Date', 'Time', 'Dates')


def time_diff(start, end):
    dt_start = datetime.datetime.combine(datetime.date.today(), start)
    dt_end = datetime.datetime.combine(datetime.date.today(), end)
    return float((dt_end - dt_start).seconds) / (60 * 60)


def models():
    return [NaiveBayesModel(), BernoulliNaiveBayesModel()]


class KaggleDataModel(object):

    def _correct_bad_coords(self, df, other_df=None):
        """ Correct when coordinates do not place crime in SF region.

        There are rows where Y == 90 placing the crime at the North Pole. When 
        this happens, estimate coordinates by 
            1) matching to other streets of the same name
            2) matching to same street but different block
                ^^^^ TODO: prefer closer blocks
            3) if a crossroad, either of the streets making the junction
            4) use middle of the District if Address cannot be cross-referenced
        """

        cols = ['Address', 'PdDistrict', 'X', 'Y']
        df_all = df
        if other_df is not None:
            df_all = pd.concat([df[cols], other_df[cols]])

        df_temp = df.copy(deep=True)
        for n, row in df[df['Y'] == 90].iterrows():

            neighbours = df_all[(df_all['Address'] == row['Address']) & 
                                (df_all['Y'] != 90)]

            # if neighbours.empty and len(row['Address'].split(' / ')) == 2:
            #     # In train and test.csv, the only bad coords occur where the 
            #     # Addresses is a crossroad (of 2 streets)
            #     regex = '|'.join(row['Address'].split(' / '))
            #     neighbours = df_all[
            #             (df_all['PdDistrict'] == row['PdDistrict']) &
            #             (df_all['Address'].str.contains(regex)) & 
            #             (df_all['Y'] != 90)]
            
            if neighbours.empty:
                neighbours = df_all[
                    df_all['PdDistrict'] == row['PdDistrict']]
            
            x_median = np.median(neighbours['X'])
            y_median = np.median(neighbours['Y'])
            df_temp.set_value(n, 'X', x_median)
            df_temp.set_value(n, 'Y', y_median)

        return df_temp


    def feature_engineer(self, is_training, filename, aux_filename=None):
        df = pd.read_csv(filename)
        aux_df = aux_filename and pd.read_csv(aux_filename)

        temp = pd.DatetimeIndex(df['Dates'])
        df['Date'] = temp.date
        df['Time'] = temp.time
        df['Dates'] = pd.to_datetime(df['Dates'])

        # df['Block'] = 'Block of' in df['Address'] and df['Address'] or ''
        # df['Junction_min'] =  ' / ' in df['Address'] and \
        #         min(df['Address'].split(' / ')) or ''
        # df['Junction_max'] =  ' / ' in df['Address'] and \
        #         max(df['Address'].split(' / ')) or ''

        df = self._correct_bad_coords(df, aux_df)
        
        if is_training:
            encoders = {}
            for c in CATEGORICAL_VARS:
                all_choices = set(df[c])
                if c == 'Address':
                    test_choices = set()
                    if aux_df is not None:
                        test_choices = set(aux_df['Address'])
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

        if is_training:
            del df['Descript']
            del df['Resolution']

            # Ensure y value is first column of the result
            cols = ['Category'] + [x for x in df.columns if x != 'Category']
            df = df[cols]

        # Scaling coordinates so they are "prettier" to human-interpretation
        df['X'] = (df['X'] + 122) * 100
        df['Y'] = (df['Y'] -  37) * 100

        del df['Dates']
        
        return df


    def load_training(self, training_filename):
        ''' For use with model_test_harness '''
        training = self.feature_engineer(True, training_filename)
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
