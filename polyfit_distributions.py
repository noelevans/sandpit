import numpy as np


def main():
    np.random.seed(0)
    bins = 50
    X = np.random.zipf(1.2, 1000)
    y = np.histogram(X[X<bins], bins, normed=True)[0]
    fn = np.polyfit(np.arange(bins), y, 3)
    print(fn)

    np.random.seed(0)
    bins = 50
    samples = 1000
    X = [np.random.zipf(1.2, samples),
         np.random.zipf(1.3, samples),
         np.random.zipf(1.5, samples)]
    y = np.array([np.histogram(x[x<bins], bins, normed=True)[0] for x in X])
    fn = np.polyfit(np.arange(bins), y.T, 3)
    print(fn)


if __name__ == '__main__':
    main()
