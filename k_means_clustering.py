import numpy as np
import operator
import random

from scipy.spatial import distance
from sklearn.cross_validation import train_test_split
from sklearn.datasets import load_iris


def normalise(dataset):
    maxes = np.max(dataset, axis=0)
    mins = np.min(dataset, axis=0)
    ranges = maxes - mins
    return (dataset - mins) / ranges


def random_group_assignment(points, k):
    return np.random.random_integers(0, k - 1, points)


def mean_centrepoint(points):
    return np.mean(points, axis=0)


def dist(a, b):
    return distance.euclidean(a,b)


def closest_centrepoint(point, centres):
    centres_to_dists = [(n, dist(c, point)) for n, c in enumerate(centres)]
    return sorted(centres_to_dists, key=operator.itemgetter(1))[0][0]


def main():
    k = len(load_iris()['target_names'])
    y = load_iris()['target']
    X = load_iris()['data']
    X = normalise(X)

    assignment = random_group_assignment(len(X), k)
    for attempt in range(20):
        centres = [mean_centrepoint(X[assignment == k_val]) for k_val in range(k)]
        new_assignment = np.apply_along_axis(closest_centrepoint, 1, X, centres)
        corrections = sum(assignment != new_assignment)
        print corrections
        if corrections == 0:
            print 'Optimal clusters identified'
            break
        assignment = new_assignment


if __name__ == '__main__':
    main()