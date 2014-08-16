import random
import pickle
import numpy  as np
import pandas as pd


INPUT_FIELDS = ['season', 'holiday', 'workingday', 'weather', 'temp', 
                'atemp', 'humidity', 'windspeed', 'month', 'hour' ]


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
    df['hour']  = map(parse_hour,  df['datetime'])
    return df
    

def select_n_of(inputs, n):
    available       = range(len(inputs))
    chosen_indicies = random.sample(available, n)
    if hasattr(inputs, 'irow'):
        return inputs.irow(chosen_indicies)
    else:
        return [inputs[i] for i in chosen_indicies]
        
        
def make_tree(fields, training):    
        
    def homogenity(field): 
        return training.groupby(field)['count'].apply(np.std).sum()
    
    def average_use_count(training):
        return training['count'].mean(1)
        
    most_influential = sorted((homogenity(f), f) for f in fields)[0][1]
    
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
        f = lambda value, opt: (value-opt) % 24
    elif pivot_name == 'month':
        f = lambda value, opt: (value-opt) % 12
    else:
        f = lambda value, opt: abs(value-opt)
    nearest = sorted((f(value, opt), opt) for opt in options)
    return nearest[0][1]


def traverse_tree(tree, test):
    if tree.leaves:
        return np.mean(tree.leaves.values())
    branch = tree.branches[choose_branch(test[tree.pivot], tree.branches.keys(), tree.pivot)]
    return traverse_tree(branch, test)
    
def grade_tree(tree, train_test):
    diffs = []
    for _, test in train_test.iterrows():
        prediction = traverse_tree(tree, test)
        actual     = test['count']
        diffs.append(abs(actual - prediction))
    return 1.0 / sum(diffs)
        
    
def make_forest():
    training   = load_and_munge_training_data('train.csv')
    evaluation = load_and_munge_training_data('test.csv')
    
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
    scores = [grade_tree(t, tt) for t, tt in zip(forest, tree_tests)]

    pickle.dump(forest, open( "forest.p", "wb"))

    pickle.dump(scores, open( "scores.p", "wb"))

 

    for e in evaluation.iterrows():
        predictions = []
        for tree, score in zip(forest, scores):
            prediction = traverse_tree(tree, e)
            predictions.append((prediction, score))
        weighted_scores = sum(p*s for p, s in predictions)
        weights = sum(s for _, s in predictions)
        print e['datetime'], round(weighted_scores / weights)
    
   
def main():
    make_forest()
    # training = load_and_munge_training_data('train.csv')
    # t = make_tree(['workingday', 'hour'], training)
    # print t

if __name__ == '__main__':
    main()
