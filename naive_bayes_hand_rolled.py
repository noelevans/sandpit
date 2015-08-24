""" Example of Gaussian Naive Bayes classifier implemented from scratch
    Originally taken from
        http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
"""

import operator
import numpy as np
import pandas as pd

from sklearn.cross_validation import train_test_split


def separate_by_class(train):
    """ For each dependent variable (last column of DF) value, map to
        corresponding rows of the DF
    """
    classifications = set(train[:, -1])
    return {c: train[train[:, -1] == c] for c in classifications}


def summarise(train_subset):
    """ Building a model for GNB entails determining the mean and standard
        deviation for each predictor in the training data for a given dependent
        classification value. Ignore the final column; the dependent
    """
    means = np.mean(train_subset[:, :-1], axis=0)
    stds = np.std(train_subset[:, :-1], axis=0)
    return np.column_stack((means, stds))


def fit(train):
    classification_to_instances = separate_by_class(train)
    return {c: summarise(i) for c, i in classification_to_instances.items()}


def gaussian_density_probability(x, mean, std):
    """ For a given value x, in a normal / Gaussian distribution with a given
        mean and std, return a result where -> 1 indicates extreme proximity to
        the mean with a wide std. Where result -> 0 indicates little proximity
        to the mean and a more narrow std
    """
    exponent = np.exp( -(np.power(x - mean, 2) / (2 * np.power(std, 2))))
    return (1 / (np.sqrt(2 * np.pi) * std)) * exponent


def calculate_class_probabilities(summaries, predictors):
    probas = {}
    for classification, class_summaries in summaries.items():
        probas[classification] = 1
        for p, (mean, std) in zip(predictors, class_summaries):
            probas[classification] *= gaussian_density_probability(p, mean, std)
    return probas


def predict(model, predictors):
    class_to_probability = calculate_class_probabilities(model, predictors)
    dict_value = operator.itemgetter(1)
    return sorted(class_to_probability.items(), key=dict_value)[-1][0]


def accuracy(tests, predictions):
    correct = sum(t[-1] == p for t, p in zip(tests, predictions))
    return correct / float(len(tests))


def main():
    filename = 'pima-indians-diabetes.data.csv'
    dataset = pd.read_csv(filename, header=None)
    train, test = train_test_split(dataset, test_size=0.33)
    split_str = 'Split %i rows into train=%i and test=%i rows'
    print split_str % (len(dataset), len(train), len(test))
    model = fit(train)

    predictions = [predict(model, t) for t in test]
    print 'Accuracy: %f' % accuracy(test, predictions)


if __name__ == '__main__':
    main()
