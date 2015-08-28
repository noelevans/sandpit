import sys
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


def mean_centre(points):
    return np.mean(points, axis=0)


def dist(a, b):
    return distance.euclidean(a, b)


def closest_centrepoint(point, centres):
    centres_to_dists = [(n, dist(c, point)) for n, c in enumerate(centres)]
    return sorted(centres_to_dists, key=operator.itemgetter(1))[0][0]


def most_similar(xs, ys):
    min_mismatch = sys.maxint
    for x in xs:
        for y in ys:
            mismatch = len(x - y) + len(y - x)
            if mismatch < min_mismatch:
                min_mismatch = mismatch
                min_pair = (x, y, mismatch)
    return min_pair


def accuracy(expected, result):
    expected_ag = {}
    result_ag = {}
    for n, e in enumerate(expected):
        expected_ag.setdefault(e, set()).add(n)
    for n, r in enumerate(result):
        result_ag.setdefault(r, set()).add(n)

    expected_sets = expected_ag.values()
    result_sets = result_ag.values()

    mismatches = 0
    while(expected_sets):
        e, r, m = most_similar(expected_sets, result_sets)
        mismatches += m
        expected_sets.remove(e)
        result_sets.remove(r)

    return mismatches




def main():
    K = len(load_iris()['target_names'])
    y = load_iris()['target']
    X = load_iris()['data']
    X = normalise(X)

    assignment = random_group_assignment(len(X), K)
    for attempt in range(20):
        centres = [mean_centre(X[assignment == k]) for k in range(K)]
        new_assignment = np.apply_along_axis(closest_centrepoint, 1, X, centres)
        corrections = sum(assignment != new_assignment)
        print 'Corrections:', corrections
        if corrections == 0:
            print 'Optimal clusters identified'
            break
        assignment = new_assignment

    print 'Mismatches:', accuracy(y, assignment)

if __name__ == '__main__':
    main()
