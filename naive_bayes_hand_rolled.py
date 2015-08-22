# Example of Naive Bayes implemented from Scratch in Python
# Taken from 
#   http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/

import csv
import random
import math

import numpy as np
import pandas as pd

from sklearn.cross_validation import train_test_split


def separateByClass(dataset):
    dependent_vars = set(dataset.iloc[:, -1])
    return {d: dataset[dataset.iloc[:, -1] == d] for d in dependent_vars}


def summarize(dataset):
    summaries = [(np.mean(attribute), np.std(attribute)) for attribute in zip(*dataset)]
    del summaries[-1]
    return summaries


def fit(dataset):
    separated = separateByClass(dataset)
    summaries = {}
    for classValue, instances in separated.iteritems():
        summaries[classValue] = summarize(instances)
    return summaries


def calculateProbability(x, mean, stdev):
    exponent = np.exp( -(np.power(x - mean, 2) / (2 * np.power(stdev, 2))))
    return (1 / (np.sqrt(2 * np.pi) * stdev)) * exponent


def calculateClassProbabilities(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.iteritems():
        probabilities[classValue] = 1
        for i, (mean, stdev) in enumerate(classSummaries):
            x = inputVector[i]
            probabilities[classValue] *= calculateProbability(x, mean, stdev)
    return probabilities

            
def predict(model, predictors):
    probabilities = calculateClassProbabilities(model, predictors)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.iteritems():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel


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