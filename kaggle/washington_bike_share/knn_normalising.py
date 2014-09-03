import datetime
import logging
import math
import random
import pandas as pd

logging.basicConfig(level=logging.INFO)

INPUT_FIELDS = ('holiday', 'workingday', 'temp', 'atemp', 'humidity',
                'windspeed', 'hour', 'day_of_year', 'day_of_week')
PERIODICS    = ('hour', 'day_of_year', 'day_of_week')
RESULT_FIELD = 'count'


def normalise(df, normalise=[]):
    mins  = dict((field, min(df[field])) for field in normalise)
    maxes = dict((field, max(df[field])) for field in normalise)
                
    for field in normalise:
        f = lambda x: float(x - mins[field]) / (maxes[field] - mins[field])
        df[field] = map(f, df[field])
        
    return df


def load_and_munge_training_data(filename):
    
    parse_hour = lambda dt: int(dt.split()[1].split(':')[0])
    parse_day_of_week = lambda dt: parse_date(dt).weekday()
    
    def parse_date(dt): 
        return datetime.date(*(int(x) for x in dt.split()[0].split('-')))
        
    def parse_day_of_year(dt):
        _date = parse_date(dt)
        year_start = datetime.date(_date.year, 1, 1)
        return (_date - year_start).days
        
    df = pd.read_csv(open(filename))
    df['hour']  = map(parse_hour, df['datetime'])
    df['day_of_year'] = map(parse_day_of_year, df['datetime'])
    df['day_of_week'] = map(parse_day_of_week, df['datetime'])
    return normalise(df, INPUT_FIELDS)


def euclidean_dist(a, b):
    diff = lambda m, n, field: (m - n) % 1 if field in PERIODICS else m - n
    return math.sqrt(sum((diff(a[f], b[f], f)**2 for f in INPUT_FIELDS)))


def shuffle(df):
    length = len(df)
    chosen_indices = random.sample(range(length), length)
    return df.irow(chosen_indices)


def most_influential(training, fields):
    
    def homogeneity(field):
        return training.groupby(field)[RESULT_FIELD].apply(np.std).sum()
    
    return sorted((homogeneity(f), f) for f in fields)[0][1]
    
def knn(vector, neighbours, k=3):
    ds = [(euclidean_dist(vector, n), n) for _, n in neighbours.iterrows()]
    return sorted(ds, key=lambda a: a[0])[:k]


def gaussian_weight(dist, sigma=12.0):
    return math.exp(-dist**2/(2*sigma**2))
    

def estimate(test, training):
    neighbour_dists = knn(test, training)
    weights = [(gaussian_weight(d), n) for d, n in neighbour_dists]
    sum_weights = sum(w for w, _ in weights)
    mean = sum(w * n[RESULT_FIELD] for w, n in weights) / sum_weights
    return int(mean)
    
    
def main():
    dry_run   = False
    all_train = load_and_munge_training_data('train.csv')
    
    if dry_run:
        train_on  = 0.6
    
        all_train = shuffle(all_train)
        split = int(train_on * len(all_train))
        train = all_train[: split]
        test  = all_train[split+1:]
    else:
        train = all_train
        test  = load_and_munge_training_data('test.csv')
            
    filename = 'knn-normalising.csv'
    with open(filename, 'w') as f:
        f.write('datetime,count\n')
        for n, t in test.iterrows():
            f.write('%s,%i\n' % (t['datetime'], estimate(t, train)))
            print '%s,%i' % (t['datetime'], estimate(t, train))

if __name__ == '__main__':
    main()
