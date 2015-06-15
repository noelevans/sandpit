import numpy as np
import pandas as pd

from sklearn import datasets
from sklearn.semi_supervised import label_propagation


train = pd.DataFrame.from_csv('dev_train_basic.csv')


digits = datasets.load_digits()
rng = np.random.RandomState(0)
indices = np.arange(len(digits.data))
rng.shuffle(indices)

X = digits.data[indices[:330]]          # same as images but shaped 64x1
y = digits.target[indices[:330]]        # represented numeral - single int
images = digits.images[indices[:330]]   # same as X but shaped 8x8

n_total_samples = len(y)
n_labeled_points = 10

unlabeled_indices = np.arange(n_total_samples)[n_labeled_points:]

y_train = np.copy(y)
y_train[unlabeled_indices] = -1

lp_model = label_propagation.LabelSpreading(gamma=0.25, max_iter=5)
lp_model.fit(X, y_train)

predicted_labels = lp_model.transduction_[unlabeled_indices]
true_labels = y[unlabeled_indices]

successes = sum(p == t for p, t in zip(predicted_labels, true_labels))
print float(successes) / len(predicted_labels)