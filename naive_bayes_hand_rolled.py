# Example of Naive Bayes implemented from Scratch in Python
# Taken from
#   http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/

import numpy as np
import pandas as pd

from sklearn.cross_validation import train_test_split


def separate_by_class(train):
    classifications = set(train[:, -1])
    return {c: train[train[:, -1] == c] for c in classifications}


def summarize(dataset):
    # means = np.mean(dataset[:, :-1], axis=0)
    # stdevs = np.std(dataset[:, :-1], axis=0)
    # return np.concatenate((np.array((ms,)), np.array((sd,))), axis=0)

    summaries = [(np.mean(attr), np.std(attr)) for attr in zip(*dataset)]
    del summaries[-1]
    return summaries


def fit(train):
    classification_to_instances = separate_by_class(train)
    return {c: summarize(i) for c, i in classification_to_instances.items()}


def calculate_probability(x, mean, stdev):
    exponent = np.exp( -(np.power(x - mean, 2) / (2 * np.power(stdev, 2))))
    return (1 / (np.sqrt(2 * np.pi) * stdev)) * exponent


def calculate_class_probabilities(summaries, predictors):
    probabilities = {}
    for classification, class_summaries in summaries.items():
        probabilities[classification] = 1
        for i, (mean, stdev) in enumerate(class_summaries):
            x = predictors[i]
            probabilities[classification] *= calculate_probability(x, mean, stdev)
    return probabilities


def predict(model, predictors):
    probabilities = calculate_class_probabilities(model, predictors)
    best_label, best_prob = None, -1
    for classification, probability in probabilities.items():
        if best_label is None or probability > best_prob:
            best_prob = probability
            best_label = classification
    return best_label


def accuracy(tests, predictions):
    correct = sum(t[-1] == p for t, p in zip(tests, predictions))
    return correct / float(len(tests))


def main():
    filename = 'pima-indians-diabetes.data.csv'
    dataset = pd.read_csv(filename, header=None)
    train, test = train_test_split(dataset, test_size=0.33)
    split_str = 'Split %i rows into train=%i and test=%i rows'
    print(split_str % (len(dataset), len(train), len(test)))
    model = fit(train)

    predictions = [predict(model, t) for t in test]
    print('Accuracy: %f' % accuracy(test, predictions))


if __name__ == '__main__':
    main()
