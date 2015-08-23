# Example of Naive Bayes implemented from Scratch in Python
# Taken from
#   http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/

import operator
import numpy as np
import pandas as pd

from sklearn.cross_validation import train_test_split


def separate_by_class(train):
    classifications = set(train[:, -1])
    return {c: train[train[:, -1] == c] for c in classifications}


def summarize(train_subset):
    means = np.mean(train_subset[:, :-1], axis=0)[np.newaxis].T
    stds = np.std(train_subset[:, :-1], axis=0)[np.newaxis].T
    return np.concatenate((means, stds), axis=1)


def fit(train):
    classification_to_instances = separate_by_class(train)
    return {c: summarize(i) for c, i in classification_to_instances.items()}


def calculate_probability(x, mean, std):
    exponent = np.exp( -(np.power(x - mean, 2) / (2 * np.power(std, 2))))
    return (1 / (np.sqrt(2 * np.pi) * std)) * exponent


def calculate_class_probabilities(summaries, predictors):
    probas = {}
    for classification, class_summaries in summaries.items():
        probas[classification] = 1
        for p, (mean, std) in zip(predictors, class_summaries):
            probas[classification] *= calculate_probability(p, mean, std)
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
