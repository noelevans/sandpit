import csv
import numpy  as np
import pandas as pd

INPUT_FIELDS      = set(['season', 'holiday', 'workingday', 'weather', 
                         'temp', 'atemp', 'humidity', 'windspeed'])
CONTINUOUS_FIELDS = set(['temp', 'atemp', 'humidity', 'windspeed'])
MANUAL_FIELDS     = set(['month', 'hour'])
DISCRETE_FIELDS   = (INPUT_FIELDS - CONTINUOUS_FIELDS).union(MANUAL_FIELDS)

OUTCOME = 'count'

def load_and_munge_training_data(filename):
    ds = pd.read_csv(open(filename))
    parse_month = lambda dt: int(dt.split('-')[1])
    parse_hour  = lambda dt: int(dt.split()[1].split(':')[0])
    ds['month'] = map(parse_month, ds['datetime'])
    ds['hour']  = map(parse_hour,  ds['datetime'])
    return ds
    
def fields_influence(training):
    
    def sum_std_deviations(field):
        return training.groupby(field)['count'].apply(np.mean).sum()
        
    return reversed(sorted((sum_std_deviations(f), f) for f in DISCRETE_FIELDS))

def main():
    training = load_and_munge_training_data('train.csv')
    print [el[1] for el in fields_influence(training)]

if __name__ == '__main__':
    main()
