# http://www.kaggle.com/c/bike-sharing-demand/

import numpy  as np
import pandas as pd


INPUT_FIELDS      = set(['season', 'holiday', 'workingday', 'weather',
                         'temp', 'atemp', 'humidity', 'windspeed'])
CONTINUOUS_FIELDS = set(['temp', 'atemp', 'humidity', 'windspeed'])
MANUAL_FIELDS     = set(['month', 'hour'])
DISCRETE_FIELDS   = (INPUT_FIELDS - CONTINUOUS_FIELDS).union(MANUAL_FIELDS)
ALL_FIELDS        = DISCRETE_FIELDS.union(CONTINUOUS_FIELDS)

INTERVAL_STEPS = 10
OUTCOME = 'count'


def load_and_munge_training_data(filename):
    df = pd.read_csv(open(filename))
    
    max_c_fields = dict((f, max(df[f])) for f in CONTINUOUS_FIELDS)
    min_c_fields = dict((f, min(df[f])) for f in CONTINUOUS_FIELDS)
    intervals    = dict((k, (max_c_fields[k]-min_c_fields[k])/INTERVAL_STEPS) for k in max_c_fields.keys())
    
    parse_month = lambda dt: int(dt.split('-')[1])
    parse_hour  = lambda dt: int(dt.split()[1].split(':')[0])
    df['month'] = map(parse_month, df['datetime'])
    df['hour']  = map(parse_hour,  df['datetime'])
    for f in CONTINUOUS_FIELDS:
        df[f+'_interval'] = map(lambda el: int((el - min_c_fields[f]) / intervals[f]), df[f])
    return df
   

def fields_influence(training):
   
    def sum_std_deviations(field):
        return training.groupby(field)['count'].apply(np.mean).sum()
       
    return reversed(sorted((sum_std_deviations(f), f) for f in ALL_FIELDS))


def main():
    
    training = load_and_munge_training_data('train.csv')
    print [el[1] for el in fields_influence(training)]


if __name__ == '__main__':
    main()
