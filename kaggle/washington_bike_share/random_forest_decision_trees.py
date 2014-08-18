import logging
import random
import cPickle
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)

INPUT_FIELDS = ['season', 'holiday', 'workingday', 'weather', 'temp', 
                'atemp', 'humidity', 'windspeed', 'month', 'hour']

RESULT_FIELD = 'registered'

class DecisionTree(object):
    
    def __init__(self, pivot=None):
        self.pivot    = pivot
        self.leaves   = {}
        self.branches = {}
        
    def add_branch(self, name, data):
        self.branches[name] = data
        
    def add_leaf(self, name, value):
        self.leaves[name] = value
        
    def __str__(self):
        return '{pivot = %s, branches = %s, leaves = %s}' % tuple(
            str(s) for s in (self.pivot, self.branches, self.leaves))


def load_and_munge_training_data(filename):
    df = pd.read_csv(open(filename))
    parse_month = lambda dt: int(dt.split('-')[1])
    parse_hour  = lambda dt: int(dt.split()[1].split(':')[0])
    df['month'] = map(parse_month, df['datetime'])
    df['hour']  = map(parse_hour, df['datetime'])
    return df
    

def select_n_of(inputs, n):
    available       = range(len(inputs))
    chosen_indices = random.sample(available, n)
    if hasattr(inputs, 'irow'):
        return inputs.irow(chosen_indices)
    else:
        return [inputs[i] for i in chosen_indices]
        
        
def make_tree(fields, training):    
        
    def homogeneity(field):
        return training.groupby(field)[RESULT_FIELD].apply(np.std).sum()
    
    def average_use_count(train):
        return train[RESULT_FIELD].mean(1)
        
    most_influential = sorted((homogeneity(f), f) for f in fields)[0][1]
    
    options = list(training[most_influential].unique())
    tree = DecisionTree(pivot=most_influential)
    for opt in options:
        selection = training[training[most_influential] == opt]
        remaining_fields = fields[:]
        remaining_fields.remove(most_influential)
        if not remaining_fields:
            tree.add_leaf(opt, average_use_count(selection))
        else:
            tree.add_branch(opt, make_tree(remaining_fields, selection))
    
    return tree


def not_set(training, selected_training):
    missing = set(training['datetime']) - set(selected_training['datetime'])
    return training[training['datetime'].isin(missing)]


def choose_branch(value, options, pivot_name):
    if value in options:
        return value
    if pivot_name == 'hour':
        f = lambda v, opt: (v - opt) % 24
    elif pivot_name == 'month':
        f = lambda v, opt: (v - opt) % 12
    else:
        f = lambda v, opt: abs(v - opt)
    nearest = sorted((f(value, opt), opt) for opt in options)
    return nearest[0][1]


def traverse_tree(tree, test):
    if tree.leaves:
        return np.mean(tree.leaves.values())
    key = choose_branch(test[tree.pivot], tree.branches.keys(), tree.pivot)
    branch = tree.branches[key]
    return traverse_tree(branch, test)


def grade_tree(tree, train_test):
    diffs = []
    for _, test in train_test.iterrows():
        prediction = traverse_tree(tree, test)
        actual     = test[RESULT_FIELD]
        diffs.append(abs(actual - prediction))
    return 1.0 / sum(diffs)
        
    
def make_forest():
    training = load_and_munge_training_data('train.csv')
    logging.info('Load of input data complete')
     
    tree_count               = int(0.1 * len(training))
    training_count_per_tree  = int(0.7 * len(training))
    training_fields_per_tree = int(0.5 * len(INPUT_FIELDS))
    
    tree_input_fields = [select_n_of(INPUT_FIELDS, training_fields_per_tree)
                         for _ in range(tree_count)]
    tree_training     = [select_n_of(training, training_count_per_tree)
                         for _ in range(tree_count)]
    tree_tests        = [not_set(training, tt)
                         for tt in tree_training]
                     
    forest = [make_tree(i, f) for i, f in zip(tree_input_fields, tree_training)]
    logging.info('Forest filled')
    
    scores = [grade_tree(t, tt) for t, tt in zip(forest, tree_tests)]
    logging.info('All trees scored')

    # cPickle.dump(forest, open('forest.p', 'wb'))
    # cPickle.dump(scores, open('scores.p', 'wb'))
    logging.info('Forest pickled')
    
    return forest, scores
    
    
def evaluate_test_data(forest, scores, file_obj):
    evaluation = load_and_munge_training_data('test.csv')
    logging.info('Load of test data complete')
    
    file_obj.write('datetime,count\n')
    for _, e in evaluation.iterrows():
        predictions = []
        for tree, score in zip(forest, scores):
            prediction = traverse_tree(tree, e)
            predictions.append((prediction, score))
        weighted_scores = sum(p * s for p, s in predictions)
        weights  = sum(s for _, s in predictions)
        estimate = round(weighted_scores / weights)
        file_obj.write('%s,%i\n' % (e['datetime'], estimate))
    
   
def main():
    use_cached_forest = False
    if use_cached_forest:
        forest = cPickle.load(open('forest.p'))
        scores = cPickle.load(open('scores.p'))
        logging.info('Used cached forest and scores')
    else:
        forest, scores = make_forest()
    
    filename = 'submission3-%s.csv' % RESULT_FIELD
    with open(filename, 'w') as file_obj:
        evaluate_test_data(forest, scores, file_obj)


if __name__ == '__main__':
    main()
