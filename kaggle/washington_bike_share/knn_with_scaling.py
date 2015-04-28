import math
import pandas as pd


INPUT_FIELDS = set(['season', 'holiday', 'workingday', 'weather',
                    'temp', 'atemp', 'humidity', 'windspeed'])
INPUT_FIELDS = set(['temp', 'humidity', 'windspeed'])


def load_and_munge_training_data(filename):
    df = pd.read_csv(open(filename))
    parse_month = lambda dt: int(dt.split('-')[1])
    parse_hour  = lambda dt: int(dt.split()[1].split(':')[0])
    df['month'] = map(parse_month, df['datetime'])
    df['hour']  = map(parse_hour,  df['datetime'])
    return df
   

def euclidean_dist(a, b):
    return math.sqrt(sum(abs(a[f] - b[f]) ** 2 for f in INPUT_FIELDS))


def knn(vector1, neighbours, k=5):
    ds = [(euclidean_dist(vector1, n), n) for _, n in neighbours.iterrows()]
    return sorted(ds, key=lambda a: a[0])[:k]


def gaussian_weight(dist, sigma=12.0):
    return math.exp(-dist ** 2 / (2 * sigma ** 2))
    

def estimate(test, training):
    neighbour_dists = knn(test, training)
    weights = [(gaussian_weight(d), n) for d, n in neighbour_dists]
    sum_weights = sum(w for w, _ in weights)
    mean = sum(w * n['count'] for w, n in weights) / sum_weights
    return int(mean)


def main():
    training = load_and_munge_training_data('train.csv')
    test_set = load_and_munge_training_data('test.csv')
    
    with open('result.csv', 'w') as f:
        f.write('datetime,count')
        for n, test in test_set.iterrows():
            f.write('%s,%i\n' % (test['datetime'], estimate(test, training)))

if __name__ == '__main__':
    main()
